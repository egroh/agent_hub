import os
import asyncio
import time
import logging
from dotenv import load_dotenv
from vapi import Vapi

from .schema import OutboundCallRequest, OutboundCallResponse

logger = logging.getLogger(__name__)


class VapiService:
    """Service pour gérer les appels Vapi"""

    def __init__(self):
        # Chargement des variables d'environnement
        load_dotenv()

        # Configuration Vapi
        api_key = os.getenv("VAPI_API_KEY")
        self.demo_mode = os.getenv("DEMO_MODE", "false").lower() == "true"

        if not api_key and not self.demo_mode:
            raise ValueError("VAPI_API_KEY environment variable is required")

        if not self.demo_mode:
            self.client = Vapi(token=api_key)
        else:
            self.client = None

        self.logger = logger

        # Configuration des IDs (tes vraies valeurs)
        self.phone_number_id = "a8e48b07-00d4-40dc-89bd-25211eaf744b"
        self.assistant_id = "ad4b6b43-8188-47b5-9c68-aa4905002264"

        # Prompt système pour l'assistant
        self.system_prompt = """
You are InsightBot, an internal voice assistant.
Your job is to give a *very short* (maximum two-sentence) recap of the latest Market Overview, then immediately ask one question to invite the listener to continue.

Guidelines:
- Be concise, friendly and confident.
- After the recap, ask something like: "Would you like to explore any point further?".
- If the listener asks follow-up questions, answer helpfully.
- Use the person's name when appropriate: {{name}}
- Keep in mind the action to take: {{action_to_take}}

Here is the Market Overview you must summarise:
{{market_overview}}
"""

    async def make_outbound_call(
        self, request: OutboundCallRequest
    ) -> OutboundCallResponse:
        """
        Déclenche un appel sortant avec la Market Overview
        """
        start_time = time.time()

        self.logger.info(f"Starting outbound call to {request.target_number}")

        try:
            if self.demo_mode:
                self.logger.info(
                    f"DEMO_MODE: Simulating outbound call to {request.target_number}"
                )
                await asyncio.sleep(1.5)
                call_id = f"demo-call-{int(time.time())}"
            else:
                # Lancement de l'appel avec les variables dynamiques
                call = self.client.calls.create(
                    assistant_id=self.assistant_id,
                    phone_number_id=self.phone_number_id,
                    customer={
                        "number": request.target_number,
                    },
                    assistant_overrides={
                        "variable_values": {
                            "market_overview": request.market_overview,
                            "name": request.name,
                            "action_to_take": request.action_to_take,
                        }
                    },
                )
                call_id = call.id

            execution_time = time.time() - start_time

            self.logger.info(f"Outbound call initiated successfully: {call_id}")

            # Métadonnées pour le suivi
            metadata = {
                "target_number": request.target_number,
                "market_overview_length": len(request.market_overview),
                "name": request.name,
                "action_to_take": request.action_to_take,
                "phone_number_id": self.phone_number_id,
                "assistant_id": self.assistant_id,
            }

            return OutboundCallResponse(
                success=True,
                call_id=call_id,
                message="Appel sortant déclenché avec succès",
                assistant_id=self.assistant_id,
                execution_time=execution_time,
                metadata=metadata,
            )

        except Exception as error:
            execution_time = time.time() - start_time
            error_message = f"Erreur lors du déclenchement de l'appel: {str(error)}"

            self.logger.error(error_message)

            return OutboundCallResponse(
                success=False,
                call_id=None,
                message=error_message,
                assistant_id=self.assistant_id,
                execution_time=execution_time,
                metadata={"error": str(error)},
            )

    async def make_simple_call(self, target_number: str) -> OutboundCallResponse:
        """
        Déclenche un appel simple sans variables dynamiques
        """
        start_time = time.time()

        self.logger.info(f"Starting simple outbound call to {target_number}")

        try:
            if self.demo_mode:
                self.logger.info(
                    f"DEMO_MODE: Simulating simple outbound call to {target_number}"
                )
                await asyncio.sleep(1.5)
                call_id = f"demo-simple-call-{int(time.time())}"
            else:
                call = self.client.calls.create(
                    assistant_id=self.assistant_id,
                    phone_number_id=self.phone_number_id,
                    customer={
                        "number": target_number,
                    },
                )
                call_id = call.id

            execution_time = time.time() - start_time

            self.logger.info(f"Simple outbound call initiated successfully: {call_id}")

            metadata = {
                "target_number": target_number,
                "phone_number_id": self.phone_number_id,
                "assistant_id": self.assistant_id,
                "call_type": "simple",
            }

            return OutboundCallResponse(
                success=True,
                call_id=call_id,
                message="Appel simple déclenché avec succès",
                assistant_id=self.assistant_id,
                execution_time=execution_time,
                metadata=metadata,
            )

        except Exception as error:
            execution_time = time.time() - start_time
            error_message = (
                f"Erreur lors du déclenchement de l'appel simple: {str(error)}"
            )

            self.logger.error(error_message)

            return OutboundCallResponse(
                success=False,
                call_id=None,
                message=error_message,
                assistant_id=self.assistant_id,
                execution_time=execution_time,
                metadata={"error": str(error), "call_type": "simple"},
            )

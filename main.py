from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from bot import consultar_portal

app = FastAPI(
    title="API Robô Portal da Transparência - MostQI",
    description="Desafio Full Stack Python - RPA e Hiperautomação",
    version="1.0"
)


class ConsultaRequest(BaseModel):
    termo: str = Field(..., min_length=1, description="Termo usado na busca do portal")
    filtro_social: bool = False


@app.post("/consultar", summary="Executa a automação no Portal da Transparência")
async def executar_robo(payload: ConsultaRequest):
    termo = payload.termo.strip()
    if not termo:
        return JSONResponse(
            status_code=400,
            content={
                "status": "erro",
                "mensagem": "Informe um termo de busca válido."
            }
        )

    resultado = await consultar_portal(termo, payload.filtro_social)

    if resultado.get("status") == "erro":
        return JSONResponse(
            status_code=400,
            content={
                "status": "erro",
                "mensagem": resultado["mensagem"]
            }
        )

    return JSONResponse(content=resultado)
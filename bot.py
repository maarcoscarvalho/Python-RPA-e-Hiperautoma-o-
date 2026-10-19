import base64
from playwright.async_api import async_playwright

PORTAL_URL = "https://portaldatransparencia.gov.br/pessoas-fisicas/busca/lista?pagina=1&tamanhoPagina=10"
MENSAGEM_ERRO_CONSULTA = "Não foi possível retornar os dados no tempo de resposta solicitado."


async def consultar_portal(termo: str, filtro_social: bool = False):
    termo_limpo = (termo or "").strip()

    if not termo_limpo:
        return {
            "status": "erro",
            "mensagem": "Informe um termo de busca válido para consultar o portal."
        }

    browser = None
    context = None

    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(viewport={"width": 1440, "height": 1200})
            page = await context.new_page()

            await page.goto(PORTAL_URL, wait_until="domcontentloaded", timeout=60000)

            content = await page.content()
            lower_content = content.lower()
            if (
                "challenge-container" in lower_content
                or "not a robot" in lower_content
                or "awswaf" in lower_content
                or "javascript is disabled" in lower_content
            ):
                return {
                    "status": "erro",
                    "mensagem": MENSAGEM_ERRO_CONSULTA
                }

            try:
                await page.get_by_role("button", name="Aceitar").click(timeout=5000)
            except Exception:
                pass

            campo_pesquisa = page.locator("input#pesquisa, input[name='pesquisa']")
            if await campo_pesquisa.count() == 0:
                return {
                    "status": "erro",
                    "mensagem": "Não foi possível localizar o campo de busca do portal."
                }

            await campo_pesquisa.fill(termo_limpo, timeout=10000)

            if filtro_social:
                filtro_elementos = page.locator(
                    "label:has-text('Beneficiário de Programa Social'), "
                    "input[type='checkbox'][name*='social' i]"
                )
                if await filtro_elementos.count() > 0:
                    await filtro_elementos.first.click(timeout=5000)

            botao_consultar = page.get_by_role("button", name="Consultar")
            try:
                await botao_consultar.click(timeout=10000)
            except Exception:
                await page.locator("button:has-text('Consultar')").click(timeout=10000)

            try:
                await page.wait_for_load_state("networkidle", timeout=15000)
            except Exception:
                pass

            resultados = page.locator("table, .tabela, .resultado, tbody")
            if await resultados.count() == 0:
                return {
                    "status": "erro",
                    "mensagem": f'Foram encontrados 0 resultados para o termo "{termo_limpo}".'
                }

            screenshot_bytes = await page.screenshot(full_page=True)
            imagem_base64 = base64.b64encode(screenshot_bytes).decode("utf-8")

            return {
                "termo_buscado": termo_limpo,
                "status": "sucesso",
                "evidencia_base64": imagem_base64,
                "detalhes": "Dados extraídos com sucesso do Portal da Transparência."
            }

        except Exception:
            return {
                "status": "erro",
                "mensagem": MENSAGEM_ERRO_CONSULTA
            }

        finally:
            if context:
                await context.close()
            if browser:
                await browser.close()
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# Para cada propiedad, solo se estan capturando Titulo, subtitulos, precio, calificacion y numero de reseñas
# y categoria de Anfitrion.
# Los datos se capturan del resultado de busqueda de la pagina web de Airbnb.
# No se encontraron datos de direccion en texto(La ubicacion se muestra en GoogleMaps).

# Funcion para capturar datos, devuelve Dataframe actualizado.
def capturaDatos(driver, df):
    itemList = driver.find_elements(By.XPATH, '//div[@itemprop="itemListElement"]')
    for item in itemList:
        try:
            titulo = item.find_element(By.XPATH, './/div[@data-testid="listing-card-title"]')
            subtitulos = item.find_elements(By.XPATH, './/div[@data-testid="listing-card-subtitle"]')
            subtitulo_text = ' | '.join([subtitulo.text.replace("\n", "|").replace("\r", "|") for subtitulo in subtitulos])

            precios = item.find_elements(By.XPATH,'.//span[@class="_1qgfaxb1"]')
            precio_text = ' | '.join([precio.text.replace("\n", "|").replace("\r", "|").replace(",", "|") for precio in precios])

            calificacion = item.find_element(By.XPATH,
                                             './/div[@class="t1a9j9y7 atm_da_1ko3t4y atm_dm_kb7nvz atm_fg_h9n0ih dir dir-ltr"]')
            cat_anfitrion = item.find_element(By.XPATH, './/div[@class="t1p13dzz atm_fg_1y6m0gg dir dir-ltr"]')

            df = pd.concat([df, pd.DataFrame({
                'Titulo': [titulo.text],
                'Subtitulo': [subtitulo_text],
                'Precio': [precio_text],
                'Calificacion': [calificacion.text.replace("\n", "|").replace("\r", "|").replace(",", "|")],
                'Cat_anfitrion': [cat_anfitrion.text.replace("\n", "|").replace("\r", "|")]
            })], ignore_index=True)

        except AttributeError:
            continue
    return df


# Configuracion de navegador
opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36")
opts.add_argument("--headless")
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=opts
)

# Se uso direccion de airbnb haciendo busqueda para Barcelona para facilitar la extracion de datos.
driver.get('https://www.airbnb.com.pe/s/Barcelona--Espa%C3%B1a/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-11-01&monthly_length=3&monthly_end_date=2024-12-01&price_filter_input_type=0&channel=EXPLORE&query=Barcelona%2C%20Espa%C3%B1a&date_picker_type=flexible_dates&source=structured_search_input_header&search_type=autocomplete_click&search_mode=regular_search&price_filter_num_nights=5&zoom_level=11&place_id=ChIJ5TCOcRaYpBIRCmZHTz37sEQ&location_bb=QiXfiUAOmEpCJUSmQANZbg%3D%3D&checkin=2024-11-04&checkout=2024-11-11&flexible_trip_dates%5B%5D=january&adults=1')
# Espera de 2 segundos hasta que los elementos web esten listos, de lo contrario no se capturan datos.
sleep(2)
df = pd.DataFrame(columns=['Titulo', 'Subtitulo','Precio','Calificacion','Cat_anfitrion'])

while len(df) < 100:
    # Captura de datos y actualizcion del DF
    df=capturaDatos(driver,df)
    try:
        # Intentar click en boton siguiente para pasar a la siguietne pagina
        next_button = driver.find_element(By.XPATH, '//a[@aria-label="Siguiente"]')
        next_button.click()
        # Espera de 2 segundos hasta que los elementos web esten listos.
        sleep(2)
    except:
        print("No se encontró el botón de siguiente o no hay más páginas.")
        break

# Guardado en archivo CSV
df.head(100).to_csv('listado_airbnb.csv', index=False)
print("Datos guardados en listado_airbnb.csv")



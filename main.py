import requests 
from bs4 import BeautifulSoup
import db
from models import Keyword
from datos import exportar_resultados_a_xlsx


def keywords_como_lista_de_valores(keywords):
    return [(kw.keywords, kw.posicion) for kw in keywords]

def aparece_el_dominio(link,dominio):
    encontrado = False
    fin = link.find('&')
    pagina = link[:fin]
    if dominio in pagina:
        encontrado = True
    return encontrado




def comprueba_keywords(kw,dominio):
    continuar = True
    start =0
    posicion = 1
    encontrado = False
    while continuar and not encontrado:
        parametros ={'q':kw,'start':start}
        resp =requests.get(f'https://www.google.com/search?q=',params =parametros)
        if resp.status_code ==200:
            soup =BeautifulSoup(resp.text,'lxml')
            div_principal = soup.find('div',{'id':'main'})
            resultados = div_principal.find_all('div',class_='ZINbbc xpd O9g5cc uUPGi')
            for res in resultados:
                if res.div and res.div.a:
                    if aparece_el_dominio(res.div.a['href'],dominio):
                        encontrado = True
                        break
                    else: 
                        posicion +=1
            if not encontrado:
                footer =div_principal.find('footer')
                siguiente = footer.find('a',{'arial-label':'Pagina siguiente'})
                if siguiente:
                    start +=10
                    if start ==100:
                        continuar =False
                else: 
                    continuar =False
        else:
            continuar = False
    if not encontrado:
        posicion =100
    return posicion

#funcion pra mostrar el menu
def muestra_menu():
    print('')
    print('')
    print('-----Kwranking-------')
    print('')
    print('[1]-Importar palabras clave')
    print('[2]-Mostrar palabras clave')
    print('[3]- Comprobar palabras clave')
    print('[4]-mostrar lista de valores')
    print('[0]-Salir')

def cargar_keywords():
    keywords =[]
    try:
        with open('keywords.txt')as fichero:
            for kw in fichero:
                kw =kw.replace('\n','').lower()
                keyword =Keyword(kw)
                keyword.save()
    except FileNotFoundError:
        print('No se encuentra ek fichero keywords.txt')
    return Keyword.get_all()

def muestra_keywords(keywords):
    contador = 0
    for kw in keywords:
        print(f'KW: {kw.keywords} >{kw.posicion}')
        contador +=1
        if contador ==20:
            contador =0
            input ('Mostrar mas...')
def run():
    keywords=Keyword.get_all()
    dominio ='youtube.com'
    while True:
        muestra_menu()
        opcion = input('Selecciona una opcion >')
        opcion = int(opcion)
        if opcion ==0:
            break
        elif opcion ==1:
            keywords =cargar_keywords()
        elif opcion ==2:
        
            muestra_keywords(keywords)
        elif opcion ==3:
            for kw in keywords:
                posicion = comprueba_keywords(kw.keywords,dominio)
                kw.posicion = posicion if posicion<100 else None
                kw.save()
        elif opcion ==4:
            kws = keywords_como_lista_de_valores(keywords)
            exportar_resultados_a_xlsx(kws)
        else:
            print('Opcion no valida')
if __name__ =='__main__':
    db.Base.metadata.create_all(db.engine)
    run()





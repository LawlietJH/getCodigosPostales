# -*- coding: utf-8 -*-

# By: LawlietJH
# Version: 1.0.2

import os, sys, json
import requests
from bs4 import BeautifulSoup



reload(sys)
sys.setdefaultencoding('utf-8')



def getCPs(municipio):
	
	cont = 0
	page2 = 'https://micodigopostal.org/' + municipio
	
	req = requests.get(page2)
	
	if req.status_code == 200:
		
		codigosPostales = {}
		
		soup = BeautifulSoup(req.text, 'html.parser')
		datos = soup.find_all('tr')
		tamDatos = len(datos)
		
		for i, x in enumerate(datos):
			
			if x.find('td') == None:
				tamDatos -= 1
				continue
			else:
				
				temp = []
				
				for j, y in enumerate(x.find_all('td')):
					temp.append(y.text)
				
				try:
					
					cp = temp[2]
					datos = {
								'colonia':	temp[0],
								'zona':		temp[5],
								'tipo':		temp[1]
							}
					
					if cp in codigosPostales:
						codigosPostales[cp].append(datos)
					else:
						codigosPostales[cp] = [datos]
					
				except IndexError:
					tamDatos -= 1
					continue
				
				cont += 1
				nombre = ', '.join(municipio[:-1].split('/')[::-1]).replace('-',' ').title().strip()
				sys.stdout.write('\r\t [+] Progreso de {}: {} de {}'.format(nombre, cont, tamDatos))
				
		return codigosPostales
		
	else:
		
		print(' [!] No se pudo conectar con la pagina: ' + page)



municipios = [
			'guanajuato/leon/',
			'guanajuato/guanajuato/',
			'aguascalientes/aguascalientes/',
			'san-luis-potosi/san-luis-potosi/',
			'queretaro/queretaro/'
		]



if __name__ == '__main__':
	
	for i, municipio in enumerate(municipios):
		
		print('\n\n\n\t [+] Municipios: {} de {}'.format(i+1, len(municipios)))
		codigosPostales = getCPs(municipio)
		js = json.dumps(codigosPostales, indent=4,
						sort_keys=True,  ensure_ascii=False)
		
		if not os.path.exists('municipios/'): os.mkdir('municipios/')
		
		name = 'municipios/'+municipio.replace('-',' ').replace('/',' - ')[:-3].title() + '.json'
		
		with open(name, 'w') as jsonFile:
			
			jsonFile.write(js)
			jsonFile.close()
			

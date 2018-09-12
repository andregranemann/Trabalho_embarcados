#!/usr/bin/python
#-*- coding: ISO-8859-1 -*-  
 
print "Content-type: text/html; ISO-8859-1"  
print  

html =	 '''<html>  
	 <head>  
		 <title>%s</title>  
	 <head>  
	 <body>  
		 <table border="0" width="100%%" cellpadding="0" cellspacing="0">
			 <tr>
				 <td height="500" valign="top">
					 <!-- conteudo -->
					 %s
				 </td>
			 </tr>
			 <tr>
				 <td align="center">
					 <!-- rodape -->
					 Programando em Python para WEB
Passo à Passo Completo by ScornInPC
				 </td>
			 </tr>
		 </table>  
	 </body>  
 <html>'''
 
titulo = "Programando em Python para WEB :: Tutorial 2"
conteudo = "Olá"
  
print html % (titulo, conteudo)

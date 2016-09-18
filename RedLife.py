#########################################RedPion#########################################
#Author : Victor MARTIN																	#
#Date : 01/2010																			#
#License : GPL v3																		#
#~ RedLife is a cellular automaton created in 2010 by Victor MARTIN with python and GTK+#
#~ Copyright (C) 2010  Victor MARTIN													#
#~ 																						#
#~ This program is free software: you can redistribute it and/or modify					#
#~ it under the terms of the GNU General Public License as published by					#
#~ the Free Software Foundation, either version 3 of the License, or					#
#~ (at your option) any later version.													#
#~ 																						#
#~ This program is distributed in the hope that it will be useful,						#
#~ but WITHOUT ANY WARRANTY; without even the implied warranty of						#
#~ MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the						#
#~ GNU General Public License for more details.											#
#~ 																						#
#~ You should have received a copy of the GNU General Public License					#
#~ along with this program.  If not, see <http://www.gnu.org/licenses/>.				#
#########################################################################################
#
#!/usr/bin/python
# -*- coding: iso-8859-1 -*-




import gtk

import pygtk
pygtk.require("2.0")



import gtk
import random
import gobject
#~ from time import *
import warnings
warnings.simplefilter("ignore")



#~ print gtk.rc_get_theme_dir(),gtk.rc_get_module_dir()
#~ print gtk.rc_get_default_files()
#~ print gtk.rc_get_im_module_file(),gtk.rc_get_im_module_path()
class RedLife(object):

	def __init__(self,i,j,inter,nb):
		
		" " " Initalisation de l'application " " "
		
		############Proprietes diverses de l'automate en lui meme############
		self.longueur=i  #Longueur du tableau
		self.largeur=j  #Largeur du tableau
		self.nbGener=nb  #Nb de generations
		self.intervalleT=inter  #Intervalles de temps en ms
		self.etat=1  #si self.etat=1, on fais une nouvelle generation de cellules tous les self.intervalleT
		self.regleM=['3']  #nb de voisins pour qu'une cellule morte vive
		self.regleV=['2','3']  #nb de voisins pour qu'une cellule vivante reste vivante
		self.tab=[[0]*self.largeur]*self.longueur  #Tableau de depart avec que des cellules mortes
		self.motifNb=0  #Motif selectionne. 0 = Aucun motif selectionne

		
		
		
		############Proprietes graphiques de l'application ############
		self.widgets = gtk.Builder()
		self.widgets.add_from_file('interface.xml')
		self["statusBar"].console_context = self["statusBar"].get_context_id('Message de la console')
		self["statusBar"].push(0, 'Generation : '+str(self.nbGener))

		self["ruler"].set_value(self.intervalleT)
		self["Alongueur"].set_value(self.longueur)
		self["Alargeur"].set_value(self.largeur)
		
		self.graphics_pour_canvas = self["canvas"].window.new_gc()
		#declaration des couleurs qui seront utilisees
		self.pinceau_rouge_pour_canvas = self.graphics_pour_canvas.get_colormap().alloc_color("#f00")
		self.pinceau_vert_pour_canvas = self.graphics_pour_canvas.get_colormap().alloc_color("#32CD32")
		
		self.autoConnect()
		self.newGeneration()
		
	def __getitem__(self, key):
		return self.widgets.get_object(key)

	def autoConnect(self):
		eventHandlers = {}
		for (itemName,value) in self.__class__.__dict__.items(): 
			if callable(value) and itemName.startswith('gtk_'):   
				eventHandlers[itemName[4:]] = getattr(self,itemName) 
		self.widgets.connect_signals(eventHandlers)
	
	
	
	def gtk_delete(self,event=None, source=None):
		gtk.main_quit()	
		
	
	
	
		
	def gtk_longlarg(self,event):
		" " " On affiche la fenetre pour modifier la taille du tableau " " " 
		
		response=self["dialog1"].run()
		
		if response != gtk.RESPONSE_NONE and response != gtk.RESPONSE_DELETE_EVENT: 
			a=int(self["Alongueur"].get_text())
			b=int(self["Alargeur"].get_text())
			gtk.main_quit()
			self["fen1"].destroy()
			self["dialog1"].destroy()
			self.etat=0
			RedLife(a,b,self.intervalleT,self.nbGener)
			gtk.main()
		self["dialog1"].hide()
	
	
	
	
	
	def gtk_regler(self,event):
		" " " On affiche la fenetre pour modifier les regles de l'automate " " " 
		

		response=self["dialog2"].run()
		print response
		if response != gtk.RESPONSE_NONE and response != gtk.RESPONSE_DELETE_EVENT:
			for i in list(self["AregleM"].get_text().replace(',','')):
				#print str(i),i,int(i),str(str(i))
				if ord(i) not in range(ord('0'),ord('9')):
					return False
			
			
			for i in list(self["AregleM"].get_text().replace(',','')):
				if ord(i) not in range(ord('0'),ord('9')):
					return False
			
			self.regleM=list(self["AregleM"].get_text().replace(',',''))
			self.regleV=list(self["AregleV"].get_text().replace(',',''))
		self["dialog2"].hide()
		

		
	
	
	
	
	
		
	def gtk_about(self, event=None, source=None):
		
		" " " Fenetre 'A propos' " " " 
		
		response = self["aboutdialog1"].run() # or however you run it
		if response == gtk.RESPONSE_DELETE_EVENT or response == gtk.RESPONSE_CANCEL:
			self["aboutdialog1"].hide()
	
	
	
	def gtk_suivant(self, event=None, source=None):
		
		" " " Etape suivante de la generation " " " 
		
		if not self["Apause"].get_active():
			self["Apause"].set_active(True)
			self.gtk_pause(event)
		self.newGeneration()
		
		
	def gtk_changeMotif(self, source=None):
		
		" " " Selectionne un nouveau motif " " " 
		
		l=source.get_group()
		i=0
		while l[i]!= source:
			i+=1
		self.motifNb=8-i
		
		
	def motif(self,Xp,Yp,etat): 
	
		" " " Affiche le motif selectionne la ou on clique " " "
		
		index=self.motifNb
		if index==1:
			#r-pentomino
			self.tab[Yp][Xp-1]=etat
			self.tab[Yp-2][Xp]=etat
			self.tab[Yp-1][Xp]=etat
			self.tab[Yp][Xp]=etat
			self.tab[Yp-1][Xp+1]=etat
		if index==6:
			#r-pentomino
			self.OldXp=Xp
			self.OldYp=0
			self.ligne(Xp,self.longueur-1,1)
		if index==7:
			#r-pentomino
			self.OldYp=Yp
			self.OldXp=Xp=0
			self.ligne(self.largeur-1,Yp,1)

		if index==2:
			#t-pentomino
			self.tab[Yp][Xp]=etat
			self.tab[Yp+1][Xp]=etat
			self.tab[Yp+2][Xp]=etat
			self.tab[Yp+1][Xp+1]=etat

		if index==3:
			#planeur
			self.tab[Yp][Xp+1]=etat
			self.tab[Yp+1][Xp+2]=etat
			self.tab[Yp+2][Xp]=etat
			self.tab[Yp+2][Xp+1]=etat
			self.tab[Yp+2][Xp+2]=etat

		if index==4:
			#vaisseau spatial
			self.tab[Yp][Xp]=etat
			self.tab[Yp+1][Xp+1]=etat
			self.tab[Yp-3][Xp+2]=etat
			self.tab[Yp+1][Xp+2]=etat
			self.tab[Yp-2][Xp+3]=etat
			self.tab[Yp-1][Xp+3]=etat
			self.tab[Yp][Xp+3]=etat
			self.tab[Yp+1][Xp+3]=etat
			
		if index==5 and Xp+17<self.largeur and Yp+4 < self.longueur:#23 26
			self.tab[Yp][Xp]=etat
			self.tab[Yp+3][Xp]=etat
			self.tab[Yp+4][Xp+1]=etat
			self.tab[Yp][Xp+2]=etat
			self.tab[Yp+4][Xp+2]=etat
			self.tab[Yp+1][Xp+3]=etat
			self.tab[Yp+2][Xp+3]=etat
			self.tab[Yp+3][Xp+3]=etat
			self.tab[Yp+4][Xp+3]=etat

			self.tab[Yp][Xp+7]=etat
			self.tab[Yp+1][Xp+8]=etat
			self.tab[Yp+2][Xp+8]=etat
			self.tab[Yp+2][Xp+9]=etat
			self.tab[Yp+2][Xp+10]=etat
			self.tab[Yp+1][Xp+11]=etat
					
			self.tab[Yp][Xp+14]=etat
			self.tab[Yp+3][Xp+14]=etat
			self.tab[Yp+4][Xp+15]=etat
			self.tab[Yp][Xp+16]=etat
			self.tab[Yp+4][Xp+16]=etat
			self.tab[Yp+1][Xp+17]=etat
			self.tab[Yp+2][Xp+17]=etat
			self.tab[Yp+3][Xp+17]=etat
			self.tab[Yp+4][Xp+17]=etat
		
		if index in [8,9,10]:
			i=1
			coeff = int(7)
			while i<len(self.tab)-1:
				j=1
				while j<len(self.tab[i])-1:
					if random.randint(0,coeff)==0:
						self.tab[i][j]=1
					j+=1
				i+=1
		self["canvas"].queue_draw()
		
		return
	
	
	def gtk_vider(self, source=None, event=None): 
	
		" " " Vide le tableau " " "
		
		i=0
		while i<len(self.tab):
			j=0
			while j<len(self.tab[i]):
				self.tab[i][j]=0
				j+=1
			i+=1
		self["canvas"].queue_draw()
	
	
	def gtk_inverser(self, source=None, event=None):
		
		" " " Inverse le tableau " " "
		
		i=1
		while i<len(self.tab)-1:
			j=1
			while j<len(self.tab[i])-1:
				self.tab[i][j]=(self.tab[i][j]+1)%2
				j+=1
			i+=1
		self["canvas"].queue_draw()
	
	
	
	def gtk_pause(self, source=None, event=None): 
	
		" " " Met en pause les generations " " " 
		
		if self["Apause"].get_active() or self.etat==1:
			#~ print "Pause"
			self.etat=0
			try:
				gobject.source_remove(self.timer)
			except:
				pass
		else:
			#~ print "lect"
			self.etat=1
			self.boucle()


	def gtk_modifVitesse(self,event=None):
		
		" " " Modifie l'intervalle entre deux generations " " " 
		
		self.intervalleT=int(self["ruler"].get_value())
		self["statusBar"].push(0, 'Generation : '+str(self.nbGener)+'  ||  Intervalle entre deux generations : '+str(self.intervalleT)+' millisecondes')
		
		

	def boucle(self): 
	
		" " " Fonction qui va appeller la fonction de nouvelle generation au bout d'un certain temps " " " 
		
		if self.etat==1: # si on a pas cliquer sur pause :
			self.timer=gobject.timeout_add(self.intervalleT, self.newGeneration)
	
	
	def gtk_clickd(self, source=None, event=None): 
	
		" " " Rend une cellule vivante la ou on clique si on a pas selectionne de motif " " " 
	 
		canvas_width = self["canvas"].window.get_size()[0]
		canvas_height = self["canvas"].window.get_size()[1]
		X=event.x
		Y=event.y
		(Xp,Yp)= (int(X*1.0/(canvas_width*1.0/self.largeur)),int(Y*1.0/(canvas_height*1.0/self.longueur)))
		if self.motifNb == 0:
			#~ print (X,Y),(Xp,Yp),(canvas_width,canvas_height)
			self.OldXp,self.OldYp=Xp,Yp
			if event.button==1 and Yp in range(1,self.longueur) and Xp in range(1,self.largeur):
				self.tab[Yp][Xp]= 1
				X,Y=int(X),int(Y)
				self["canvas"].queue_draw_area(X-10,Y-10,X+10,Y+10)
			elif event.button==3 and Yp in range(1,self.longueur) and Xp in range(1,self.largeur):
				self.tab[Yp][Xp]= 0
				X,Y=int(X),int(Y)
				self["canvas"].queue_draw_area(X-10,Y-10,X+10,Y+10)
		else:
			if event.button !=2:
				self.motif(Xp,Yp,1)



	def gtk_move(self, source=None, event=None):
		
		" " " Rend les cellules vivantes la ou on bouge la souris, si on a pas selectionne de motif " " "
		
		canvas_width = self["canvas"].window.get_size()[0]
		canvas_height = self["canvas"].window.get_size()[1]
		
		if event.is_hint:
			x, y, state = event.window.get_pointer()
		else:
			x = event.x
			y = event.y
			state = event.state
		
		(Xp,Yp)= (int(x*1.0/(canvas_width*1.0/self.largeur)),int(y*1.0/(canvas_height*1.0/self.longueur)))
		if self.motifNb == 0:
			if Yp in range(1,self.longueur) and Xp in range(1,self.largeur):
				if state & gtk.gdk.BUTTON1_MASK:
					self.tab[Yp][Xp]= 1
					self.ligne(Xp,Yp,1)
					self["canvas"].queue_draw()
					#~ print x,y,(self.OldXp,self.OldYp,Xp,Yp)
				elif state & gtk.gdk.BUTTON3_MASK:
					self.tab[Yp][Xp]= 0
					self.ligne(Xp,Yp,0)
					self["canvas"].queue_draw()
				self.OldXp,self.OldYp=Xp,Yp
	
	
	
	def ligne(self,Xp,Yp,etat): 
		
		" " " Quand on bouge la souris sur la zone de dessin, le programme ne va pas prendre tous les valeurs sur lesquelles est passee la souris. Alors, on trace une ligne entre la valeur precedente et la valeur actuelle pour faire 'semblant' que les cellules sont rendus vivantes la on bouge la souris. " " " 
		
		if self.OldXp-Xp<0:
			a=(self.OldYp-Yp*1.0)/(self.OldXp-Xp)
			b=Yp-(a*Xp)
			i,j=self.OldXp,self.OldYp
			while (i,j) != (Xp,Yp):
				self.tab[j][i]=etat
				i+=1
				j=int(round(a*i+b))
			self.tab[j][i]=etat
		elif self.OldXp-Xp==0:
			i,j=self.OldXp,self.OldYp
			if self.OldYp-Yp<=0:
				while j != Yp:
					self.tab[j][i]=etat
					j+=1
			else:
				while j != Yp:
					self.tab[j][i]=etat
					j-=1
			self.tab[j][i]=etat
		else:
			a=(self.OldYp-Yp*1.0)/(self.OldXp-Xp)
			b=Yp-(a*Xp)
			i,j=self.OldXp,self.OldYp
			while (i,j) != (Xp,Yp):
				self.tab[j][i]=etat
				i-=1
				j=int(round(a*i+b))
			self.tab[j][i]=etat

	


   
	def gtk_fill_canvas(self, canvas, event): 
	
		" " " Remplit la zone de dessin en se servant du tableau " " " 
	

		tabl=self.tab
		#~ self["canvas"].modify_bg(gtk.STATE_NORMAL,self.pinceau_noir_pour_canvas)
		canvas_width = self["canvas"].window.get_size()[0]
		canvas_height = self["canvas"].window.get_size()[1]
		self.graphics_pour_canvas.set_foreground(self.pinceau_vert_pour_canvas)
		self["canvas"].window.draw_line(self.graphics_pour_canvas, 0,0, canvas_width-3,0)
		self["canvas"].window.draw_line(self.graphics_pour_canvas, 0,0, 0,canvas_height-3)
		self["canvas"].window.draw_line(self.graphics_pour_canvas, canvas_width-3,0, canvas_width-3,canvas_height-3)
		self["canvas"].window.draw_line(self.graphics_pour_canvas, 0,canvas_height-3, canvas_width-3,canvas_height-3)
		
		rectH=(canvas_height*1.0)/self.longueur
		rectL=(canvas_width*1.0)/self.largeur
		
		#~ print (canvas_width ,canvas_height),self["fen1"].get_size()
		
		self.graphics_pour_canvas.set_foreground(self.pinceau_rouge_pour_canvas)
		i=1
		while i<self.longueur-1:
			j=1
			while j<self.largeur-1:
				if tabl[i][j]==1:
					self["canvas"].window.draw_rectangle(self.graphics_pour_canvas,True, int(round(rectL*j))-1,int(round(rectH*i))-1, int(rectL)+1,int(rectH)+1)
				j+=1
			i+=1
		return False
	

	def gtk_configure_canvas(self, canvas, event):  #Configuration du canvas/Declaration des outils


	
		return False
		
		
	def newGeneration(self):  
	
		" " " Fonction la plus importante du programme : elle prend un tableau en entree et applique les regles de l'automate (par defaut, celles du jeu de la vie). " " " 
		newTab=[[0]*self.largeur]
		i=1
		while i<len(self.tab)-1:
			newLigne=[0]
			j=1
			while j<len(self.tab[i])-1:
				nbVoisins=0
				if self.tab[i][j+1]==1:#A droite
					nbVoisins+=1
				if self.tab[i][j-1]==1:#A gauche
					nbVoisins+=1
				if self.tab[i+1][j]==1:#En haut
					nbVoisins+=1
				if self.tab[i-1][j]==1:#En bas
					nbVoisins+=1
				if self.tab[i+1][j+1]==1:#Diagonale
					nbVoisins+=1
				if self.tab[i-1][j+1]==1:
					nbVoisins+=1
				if self.tab[i+1][j-1]==1:
					nbVoisins+=1
				if self.tab[i-1][j-1]==1:
					nbVoisins+=1
				
				if self.tab[i][j]==0:
					if str(nbVoisins) in self.regleM:
						newLigne+=[1]
					else:
						newLigne+=[0]
				else:
					if str(nbVoisins) in self.regleV:
						newLigne+=[1]
					else:
						newLigne+=[0]
				j+=1
			newTab+=[newLigne+[0]]
			i+=1
		newTab+=[[0]*self.largeur]
		self.tab=newTab
		self.nbGener+=1
		
		#Quand la fenetre est detruite, la fonction newGeneration s'execute une derniere fois, donc quand je demande l'acces a des objets de la fenetre (canvas et statusBar), il y a une erreur car elle est detruite. Try permet d'eviter l'affichage de cette erreur.
		try:
			self["statusBar"].push(0, 'Generation : '+str(self.nbGener)+'  ||  Intervalle entre deux generations : '+str(self.intervalleT)+' millisecondes')
			self["canvas"].queue_draw()
		except:
			pass
		
		self.boucle()

	

if __name__ == '__main__':
	RedLife(100,100,1000,0)#tableau de 100*100, intervalle de 1000ms et nombre de generations a 0
	gtk.main()

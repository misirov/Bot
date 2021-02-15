# By PM.
# Free to use and modify.

import configparser
import time
import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class Bot:
	config = configparser.ConfigParser()
	config.read("accounts.ini")

	def __init__(self):
		self.prefix = "https://"

	def help(self):
		print("""
			Available Functions: 
			\n.help() : show this page 
			\n.get_html(url) :  print url's HTML code. 
			\n.add_accounts() : Generate 'accounts.ini' file with account login information 
			\n.login_account(domain, login, password) : Unless login details are stored in 'accounts.ini' file, this information must be provided.

			""" )
	# Print a webites HTML Code
	def get_html(self, url):
		try:
			r = requests.get("{}{}".format(self.prefix, url))
			soup = BeautifulSoup(r.text, "html.parser")
			print(soup)
		except:
			print("An error has occured. Invalid search or broken link.")

	# Create / add to accounts.ini file for configuration purposes
	def add_accounts(self):
		print("Enter the following information to save to the file:")
		flag = True
		while flag:
			config = configparser.ConfigParser()
			site = input("- site: ")
			username = input("- username: ")
			password = input("- password: ")
			config[site] = {"username" : username, "password" : password}

			try: # Check if file already exists on the same directory, else generate a new one
				if os.path.isfile("accounts.ini"):
					with open("accounts.ini", "a") as f:
						config.write(f)
				else:
					with open("accounts.ini", "w") as f:
						config.write(f)
			except:
				print("An error occurred while creating or writing the configuration file")

			print("1) Add more? [Y/N]")
			choice = input("> ")
			choice.lower()
			if choice == "n":
				flag = False
			else:
				flag = True

		print("\nAccount added!")


	def login_account(self, domain, username = None, password = None):
		domain = domain.lower()
		driver = webdriver.Chrome('') # Insert PATH to chromedriver

		# INSTAGRAM 
		if 'instagram' in domain:
			try:
				print(f"Going to {domain} . . .")
				login = "instagram.com/accounts/login/?"
				driver.get(f"{self.prefix}{login}")
				# Sleeping allows browser to load resources
				time.sleep(2)
				accept_cookies = driver.find_element_by_xpath("/html/body/div[2]/div/div/div/div[2]/button[1]").click()
				time.sleep(1)
				username_field = driver.find_element_by_name("username").send_keys(username)
				password_field = driver.find_element_by_name("password").send_keys(password)
				time.sleep(1)
				login = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div/div[1]/div/form/div/div[3]/button/div").click()
				driver.get(f"https://www.instagram.com/{username}/")
				
				print("Login successfull")
				print("Available options: q) quit\nD) Download users data ")
				while True:
					choice = input("> ")
					if choice == 'q':
						driver.close()
						print("Closing instagram. Back to main menu...")
						break
					else:
						print("Invalid option or not yet available")
			except:
				print("An error has occurred. Make sure username and password are correct.")
				driver.close()





		# FACEBOOK
		elif 'facebook' in domain:
			try:
				print(f"Going to {domain} . . .")
				login = "en-gb.facebook.com/login/"
				driver.get(f"{self.prefix}{login}")
				accept_cookies = driver.find_element_by_xpath("/html/body/div[3]/div[2]/div/div/div/div/div[3]/button[2]").click()
				email_field = driver.find_element_by_name("email").send_keys(username)
				password_field = driver.find_element_by_name("pass").send_keys(password)
				time.sleep(1)
				login = driver.find_element_by_name("login").click()

				print("Login successfull")
			except:
				print("An error has occurred. Make sure username and password are correct.")
				driver.close()



		# elif 'discord' in domain:
		# 	try:
		# 		print(f"Going to {domain} . . .")
		# 		login = "discord.com/login"
		# 		self.driver.get(f"{self.prefix}{login}")
		# 	except:
		# 		raise


## MAIN ##

bot = Bot()
Flag = True
while Flag:
	print("""Several options are available at the moment: 
	0) Help
	1) Print a site's HTML code
	2) Login to instagram
	3) Login to Facebook
	4) Make accounts file
	To quit the program press 'q'.
	""")
	get = input('> ')
	if get == "0":
		bot.help()

	elif get == "1":
		url = input("Enter domain, ex: google.com\n>  ")
		bot.get_html(url)

	elif get == '2':
		option = input("Use accounts file? [Y/N]")
		option.lower()
		if option == 'n':
			username = input("- username: ")
			password = input("- password: ")
			bot.login_account("instagram", username, password)

		elif option == 'y':
			

	elif get == '3':
		email = input("- email: ")
		password = input("- password: ")
		bot.login_account("facebook", email, password)

	elif get == '4':
		bot.add_accounts()
	elif get == 'q':
		Flag = False
	
	else:
		print("Invalid option.")


print("\nExited successfully ")
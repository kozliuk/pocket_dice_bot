import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import date
import time




# mhhmh needed for my security
def checkRights():
	today = date.today()
	
	expires = date(2016, 5, 2)
	expires_before = date(2016,4,23)
	
	if (today < expires) and (expires_before < today):
		print("\n\t " + today.isoformat() + " || k3n0b1-> ok.")
		return False

	print("\n\t " + today.isoformat() + " || k3n0b1-> failed.")
	print("\t Misha Kozliuk VK : http://vk.com/missshanya")
	return True

# checkQuestion Are you ready for crime?
def mainQuestion():
	answer = input("Are you ready for crime? (y/n): ")
	
	if (answer == "y"):
		return False
	
	print("Bye ... ")
	
	return True

# start emulator of FireFox
# RETURNS driver
def startFireFoxPocketDice():
	driver = webdriver.Firefox()
	driver.get("https://pocketdice.io/")
	
	return driver

# configuration PocketDice Bets!
# RETURNS list of configurations for bot
def configurationForPocketBets(driver):
	input("\nClose startup PocketDice window pls and login. Then enter for continue...")
	input("Please configure stats for bets in FirefoxWindow..")
	print("\n******************************************************")
	quantity = input("Please enter quantity of iterations: ")
	increment = input("Input the increment for iteration. : ")
	start_bet_size = driver.find_element_by_xpath("//*[@id='application-wrapper']/ng-include/div/footer/div[3]/div[2]/div[2]/input").get_attribute('value').encode('utf-8') 

	return [int(quantity), float(increment), float(start_bet_size)]

# function that shows configuration
def showConfiguration(driver, confList):

	def isFirstSelectedButton(driver):
		className = driver.find_element_by_xpath("//*[@id='application-wrapper']/ng-include/div/div[1]/div/div/div[3]/div[1]/div[1]/button[1]").get_attribute('class')
		if "selected" in className:
			return True
		return False

	if isFirstSelectedButton(driver):
		selButtonText = "Greater than"
	else:
		selButtonText = "Less than"

	number = driver.find_element_by_xpath("//*[@id='application-wrapper']/ng-include/div/div[1]/div/div/div[3]/div[1]/div[3]/div/p").text

	print("\n******************************************************")
	print("\n\tActive configuration: ")
	print(selButtonText + " " + number)
	print("Quantity of iterations: " + str(confList[0]))
	print("Increment coef. : " + str("%.5f" % confList[1]))
	print("Starting bet size: " + str("%.5f" % confList[2]))
	print("Scroll to bottom site with PoketDice :)")
	print("******************************************************")
	
# start iterations
def startIterations(driver, confList, totalWin, interestList, maxSpent):
	
	showConfiguration(driver, confList)

	t1 = time.time()

	def maxSpentMoney(totalWin, maxSp):
		if totalWin < maxSp:
			maxSp = totalWin
		return maxSp

	def timeOfIterations(t2, t1):
		return (t2 - t1)/60

	def floatResult(text):
		result = float(text[1:])
		if text.startswith("-"):
			return -1*result
		return result

	click_on_roll = driver.find_element_by_xpath("//*[@id='application-wrapper']/ng-include/div/footer/div[3]/div[1]/button[4]")
	click_on_roll.click()
	bet_size = driver.find_element_by_xpath("//*[@id='application-wrapper']/ng-include/div/footer/div[3]/div[2]/div[2]/input")
	i = 1
	interestInt = 1
	start_bet_size = confList[2]
	new_bet_size = start_bet_size
	print("\n")
	
	while (i < confList[0]):
		
		result = driver.find_element_by_xpath("//*[@id='application-wrapper']/ng-include/div/div[1]/div/div/div[2]/div[3]/div[1]/ng-include/div[2]/div[1]/ng-include/div/table/tbody/tr/td[6]/span")
		result_starts_with_minus = result.text.startswith("-")
		totalWin = totalWin + floatResult(result.text)
		maxSpent = maxSpentMoney(totalWin, maxSpent)
		#for test
		#print(result.text)
		
		
		print("Iteration: " + str(i) + " -> Result: " + result.text + " | TotalWin : " + str("%.5f" % totalWin))
		try:
			if result_starts_with_minus:
				new_bet_size = new_bet_size + confList[1]
				bet_size.clear()
				bet_size.send_keys(str('%.5f' % new_bet_size))
				
				interestInt += 1 

				click_on_roll.click()
				
			else:
				time.sleep(0.5)
				new_bet_size = start_bet_size
				bet_size.clear()
				bet_size.send_keys(str('%.5f' % new_bet_size))
				
				interestList.append(interestInt)
				interestInt = 1

				click_on_roll.click()

		except selenium.common.exceptions.WebDriverException:
			time.sleep(32)
			time.sleep(1)
			click_on_roll.click()
		
		time.sleep(0.5)
		i+=1
	
	result = driver.find_element_by_xpath("//*[@id='application-wrapper']/ng-include/div/div[1]/div/div/div[2]/div[3]/div[1]/ng-include/div[2]/div[1]/ng-include/div/table/tbody/tr/td[6]/span")
	totalWin = totalWin + floatResult(result.text)
	print("Iteration: " + str(i) + " -> Result: " + result.text + " | TotalWin : " + str("%.5f" % totalWin))
	
	t2 = time.time()
	resTime = timeOfIterations(t2, t1)
	print("Total time ellapsed: " + str(resTime))
	
	maxSpent = maxSpentMoney(totalWin, maxSpent)
	print("Max needed money: " + str("%.5f" % maxSpent))
	
	tooManyIterations(driver, totalWin, interestList, maxSpent)

# additional iterations
def tooManyIterations(driver, totalWin, interestList, mSpent):
	print("\nList of winning indexes: " + str(interestList) + "\n")
	tooManyIterations = input("\nMore iterations? (y/n): ")
	if tooManyIterations != "y":
		return 
	
	print("\n******************************************************")
	quantity = input("Please enter quantity of iterations: ")
	increment = input("Input the increment for iteration. : ")
	start_bet_size = driver.find_element_by_xpath("//*[@id='application-wrapper']/ng-include/div/footer/div[3]/div[2]/div[2]/input").get_attribute('value').encode('utf-8')
	
	conf = [int(quantity), float(increment), float(start_bet_size)]
	
	
	startIterations(driver, conf, float(totalWin), interestList, mSpent)

# close FireFox after using
def closeFireFox(driver):
	input("\nPlease enter for exit from FIREFOX!")
	driver.close()

# main 
def main():
	if checkRights():
		return 	
	if mainQuestion():
		return
	
	#statistics for me
	maxSpent = 0
	totalWin = 0
	interestingList = []
	
	driver = startFireFoxPocketDice()
	conf = configurationForPocketBets(driver)	
	
	startIterations(driver, conf, totalWin, interestingList, maxSpent)

	closeFireFox(driver)


# main point of program 
if __name__ == "__main__":
	main()









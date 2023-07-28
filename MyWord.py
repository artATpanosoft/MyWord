            
        winMessage = ["","","","","","",""]
        winMessage[1] ="Unbelievable:  Genius or Luck?"
        winMessage[2] ="Truly Exceptional:  Nice playing!"
        winMessage[3] ="Excellent!  You are making your case for Genius."
        winMessage[4] ="Very efficient.  You have the skills for this game."
        winMessage[5] ="That was a difficult word.  Good work!"
        winMessage[6] ="Nice!  You were running out of options."
        loseMessage   ="Ooooo That one slipped away.  Try again."
        badWord       ="Your guess is not an allowable word.  Use BackSpace key to try again."       
        startMessage  ="Click [Start]; Use keyboard to enter guess.  Click [Hint] for letter."       

        row=1                                     
        col=1                                     
        win = False                               
        start = False                             
        guess = ""                                # current user guess                        
        previousGuess = ""                              
        word  = "."                               # secret word                               
        code = ""                                 # code for secret word (found in url)       
        allowed = True                            # True if word is in allowed list           
        secret = True                             # True if secret word has not been revealed 
        sending = False                           # True if creating a link to MyWord!        

        def hint():                               
            global secret, word, previousGuess                      
            secret = not secret                          
            button_id = "Hint"                     
            hintButton = Element(button_id)            
            if secret:                                   
               hintButton.write("Hint")  
            else:                                        
               hint = ""                
               for x in range(0,5):                    
                   if previousGuess.find(word[x]) == -1:     
                       hint += word[x]                     
               if len(hint) > 0:                       
                   h = random.choice(hint)             
                   hintButton.write(h)                  
               else:                                   
                   hintButton.write("No Hint")       

        def start_stop():                            
            global start                             
            start = not start                        
            upper_wordList()                         
            select_word()                            
            reset_keyboard()                         
            button_id = "StartStop"                  
            startButton = Element(button_id)         
            if start:                                
               startButton.write("Reset")  
            else:                                    
               startButton.write("Start")       
               reset_game()                          

        def upper_wordList():                  
          global wordList                         
          for j in range(0,len(wordList)):        
                wordList[j] = wordList[j].upper()  

        def select_word():                                    
            global word, code, wordList                       
            urlString = window.location.href                  
            x = urlString.find("?code=")                      
            if x > 0:                                         
                c = urlString[x+6:x+11]                       
                code = c                                      
                decode_code()                                 

            if word == ".":              # word not found in url                         
                while word[0] == ".":    # Keep picking until the first letter isn't "." 
                    word = wordList[random.randint(0, len(wordList)-1)]  # pick random   

        def encode_word():                
            global word, code             #     ?code=+136/                         

            s = ""                        
            for x in range(0,5):          
                s += str(ord(word[x]))    #   "AGILE" -->  "6571737669"                  
            y = int(s)                    #   make it an integer                         
            y -= 2222222222               #   subtract 2,222,222,222  == 4349515447      
            y_str = str(y)                #   "4349515447"                               
            s = ""                                                                       
            for x in range(0,10,2):            #   0,2,4,6,8                             
                s += chr(int(y_str[x:x+2]))    #   "+136/"                               
            code = s                      #                                              

        def decode_code():                
            global word, code             

            s = ""                        
            for x in range(0,5):          
                s += str(ord(code[x]))    #   "+136/" -->  "4349515447"                   
            y = int(s)                    #   make it an integer                          
            y += 2222222222               #   add 2,222,222,222  == 6571737669            
            y_str = str(y)                #   "6571737669"                                
            s = ""                                                                        
            for x in range(0,10,2):        #   1,3,5,7,9                                  
                mid = y_str[x:x+2]         #   65, 71, 73, 76, 69                         
                midnum = int(mid)                                                         
                midchar = chr(midnum)      #    A, G, I, L, E                             
                s += midchar               #   "+136/"   -->    "AGILE"                   
            word = s                       #                                              

        def key_click(k:int):
            global row, col, start, guess, win, sending                       
            global allowed, previousGuess, secret, code, word                 

            if not start:                                                     
               start_stop()                                                   

            if sending and (k == 13):                                    
               word = previousGuess                        
               encode_word()                               
               url = "https://artatpanosoft.github.io/MyWord/?code="+code     
               show_message("SEND THIS LINK: "+url)                           
               sending = False                                                
               return                                                         

            secret = False                                                    
            hint()                                                            
            show_message(startMessage)                                        
            if (k == 8):                        # BS                          
               if (col == 1):                                                 
                  return                        # do nothing                  
               else:                                                          
                  print_letter(row,col-1,32)    # print space over letter     
                  col -= 1                      # set col back one            
                  guess = guess[:-1]            # remove letter from guess    
                  return                                                      
            if (k == 13):                       # [return]                    
               if (col == 6):                   # submit guess                
                  checkGuess(guess)             # check for win               
                  if win:                                                     
                     return                     #                             
                  if not allowed:                                             
                     allowed = True             #                             
                     return                                                   
                  else:                                                       
                     previousGuess = guess                                    
                     guess = ""                       
                     row += 1                         
                     col = 1                          
                     if row == 7:                     
                         lose_game()                  
               else:                            #                             
                  return                        # ignore [submit] until col=6 
            else:                               # some character              
               if col == 6:                     # already 5 characters        
                  return                        # wait for submit             
               else:                            #                             
                  guess += chr(k)                  # add character to guess      
                  print_letter(row,col,k)          # print character             
                  col += 1                         # move to next column         

        def lose_game():                         
            global loseMessage , word            
            show_message(loseMessage+" My word was "+word+".")   
            return                               

        def reset_game():                        
            global col, row, win, guess, start, word   
            global startMessage                  

            col = 1                              
            row = 1                              
            win = False                          
            start = False                        
            guess = ""                           
            previousGuess = ""                   
            word  = "."                          
            secret = False                       
            reset_keyboard()                     
            reset_gameboard()                    
            show_message(startMessage)           

        def reset_keyboard():                    
            color_key(8, "Blue")            
            color_key(13, "Blue")           
            for k in range(65,91):               
                 color_key(k, "Blue")

        def reset_gameboard():                       
            for row in range(1,7):                   
               for col in range(1,6):                
                   print_letter(row,col,32)               # write space         
                   color_letter(row, col, "LightBlue")    # color the letter    


        def print_letter(r:int, c:int, k:int):       
            letter_id = "row_"+str(r)+"_"+str(c)     
            letter = chr(k)                          
            myCell = Element(letter_id)              
            myCell.write(letter)                     

        def checkGuess(userGuess):
            global row, col, word, win, wordList, allowed         
            global badWord, winMessage, loseMessage               

            if userGuess in wordList:                                     
                allowed = True                                            
            else:                                                         
                show_message(userGuess + ": " + badWord)                  
                allowed = False                                           
                return                                                                           

            guessColourCode = ["grey", "grey", "grey", "grey", "grey"]   # colors start as grey  
            greenMatch  = [False, False, False, False, False]  # find and eliminate matches first
            yellowMatch = [False, False, False, False, False]  # True: letter "matches" from afar
            for x in range(0,5):                          # 0,1,2,3,4 position in word & guess   
                if word[x] == userGuess[x]:               # if there is a match                  
                    guessColourCode[x] = "green"          # ... the letter is green              
                    greenMatch[x] = True                  # ... and greenMatch=true for x        
            for x in range(0,5):                          # 0,1,2,3,4 position in guess          
                if not greenMatch[x]:                     # if no exact match at (x)             
                    if userGuess[x] in word:              # ... if guess letter in the secret word
                        for y in range(0,5):              # 0,1,2,3,4 in the secret word
                            if word[y] == userGuess[x]:   # if yth letter of word is this letter 
                                if not greenMatch[y]:     # ..and the yth secret letter not exact matched 
                                    if not yellowMatch[y]:  # ..and the yth secret letter not afar matched 
                                        guessColourCode[x] = "yellow"# Then xth guess letter is yellow match 
                                        yellowMatch[y] = True  # .. now yth secret letter has yellow match  

            for x in range(0,5):                          # 0,1,2,3,4 position in guess            
                color_letter(row, (x+1), guessColourCode[x])    # color the letter                 
                a = ord(userGuess[x])                     # ascii value of letter gives id of key  
                color_key(a, guessColourCode[x])          #       color the key                    

            if (userGuess == word):                                                                
                win = True                                                                         
                show_message(winMessage[row])                                                      

        def color_letter(r:int, c:int, color: str):
            letter_id = "row_"+str(r)+"_"+str(c)
            document.getElementById(letter_id).style.backgroundColor = color

        def color_key(k:int, color:str):
            key_id = "K"+str(k)
            document.getElementById(key_id).style.backgroundColor = color

        def show_message(m: str):                                                                
            myCell = Element("message")              
            myCell.write(m)                     
                                                                        
        def send_word():                                                                
            global sending                                  
            reset_game()                                    
            show_message("<b>Enter YOUR WORD in the top row and press [Enter]</b>")                                
            sending = True              

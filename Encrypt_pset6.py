import string

### DO NOT MODIFY THIS FUNCTION ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    print('Loading word list from file...')
    # inFile: file
    in_file = open(file_name, 'r')
    # line: string
    line = in_file.readline()
    # word_list: list of strings
    word_list = line.split()
    print('  ', len(word_list), 'words loaded.')
    in_file.close()
    return word_list

### DO NOT MODIFY THIS FUNCTION ###
def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list

### DO NOT MODIFY THIS FUNCTION ###
def get_story_string():
    """
    Returns: a joke in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story



class Message(object):
    ### DO NOT MODIFY THIS METHOD ###
    def __init__(self, text):
        '''
        Initializes a Message object
                
        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words
        '''
        self.message_text = text
        #self.valid_words = load_words(WORDLIST_FILENAME)

    ### DO NOT MODIFY THIS METHOD ###
    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text

    ### DO NOT MODIFY THIS METHOD ###
    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class
        
        Returns: a COPY of self.valid_words
        '''
        return self.valid_words[:]
        
    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.        
        
        shift (integer): the amount by which to shift every letter of the 
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        alphabet=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        dic={}
        shift_dicNum={}
        shift_dic={}
        j=1
        n=1+shift
        for letter in alphabet:
            dic[j]=letter
            j+=1
        for i in range(1,27):
            shift_dicNum[i]=dic[n]
            if n<26:
                n+=1
            elif n==26:
                n=1
        n=27+shift
        for i in range(27,53):
            shift_dicNum[i]=dic[n]
            if n<52:
                n+=1
            elif n==52:
                n=27
        for key in shift_dicNum:
            shift_dic[dic[key]]=shift_dicNum[key]
        return shift_dic
        
    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift        
        
        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''
        message_shiftL=[]
        shift_dic=Message.build_shift_dict(self,shift)
        message_shift=""
        for char in self.message_text:
            try: 
               message_shiftL.append(shift_dic[char])
            except KeyError:
                message_shiftL.append(char)
        message_shift=message_shift.join(message_shiftL)
        return message_shift
                          
class PlaintextMessage(Message):
     '''
        Initializes a PlaintextMessage object        
        
        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encrypting_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        Hint: consider using the parent class constructor so less 
        code is repeated
        '''
     
     def __init__(self, text, shift,encrypting_dict={}):
        Message.__init__(self,text)
        self.text=text
        self.shift=shift
        self.encrypting_dict=encrypting_dict

     def get_shift(self):
        '''
        Used to safely access self.shift outside of the class
        
        Returns: self.shift
        '''
        return self.shift

     def get_encrypting_dict(self):
        '''
        Used to safely access a copy self.encrypting_dict outside of the class
        
        Returns: a COPY of self.encrypting_dict
        '''
        self.encrypting_dict=Message.build_shift_dict(self,self.shift)
        return self.encrypting_dict.copy()
     def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class
        
        Returns: self.message_text_encrypted
        '''
        return Message.apply_shift(self, self.shift)

     def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other 
        attributes determined by shift (ie. self.encrypting_dict and 
        message_text_encrypted).
        
        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        self.shift=shift
class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object
                
        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        Message.__init__(self,text)
        
        self.text=text

    def decrypt_message(self):
    
        cont_words=0
        dic1={}
        wordList=[]
        def apply_shift(self,shift):
            return Message.apply_shift(self,shift)
        
        for s in range(1,27):
            shift=26-s
            test=Message.apply_shift(self,shift)
            wordList=test.split()
            for word in wordList:
                if is_word(word_list,word)==True:
                    cont_words+=1
            dic1[s]=cont_words
            cont_words=0
            wordList=[]
        values=dic1.values()
        maxi=max(values)
        for key in dic1:
            if dic1[key]==maxi:
                s=key
                break
        best=(26-s,Message.apply_shift(self,26-s))
        return best

t=True
while t==True:
    a=True
    while a==True:
      user=input("Please enter 'e' to encrypt or 'd' to decrypt: ")
      try:
         if user=="e" or user=="d":
             a=False
         else:
             raise AssertionError
      except:
        print("Please enter a valid input")
    if user=="e":
        start="start"
        while start=="start":
            try:
              message=str(input("Please enter the word you want to encrypt: "))
              shift=int(input("Please enter an integer < 26 to applay the shift: "))
              if shift>26:
                  raise AssertionError
              plaintext=PlaintextMessage(message,shift)
              print("String encrypted: ",plaintext.get_message_text_encrypted())
              start=0
            except:
                print("Please enter a valid input")
                
    if user=="d":
        a=1
        while a==1:
            try:
              message=input("Please enter the word you want to decrypt: ")
              shift=int(input("Please enter the integer used to encrypt the text: "))
              if shift>26:
                  raise AssertionError
              message=Message(message)
              print("Decrypted text: ",message.apply_shift(26-shift))
              a=0
            except:
                  print("Please enter a valid input")
    
    a=1
    while a==1:
      try:
        ans=input("Do you want to decrypt or encryp anything else? y/n: ")
        if ans=="y" or ans=="n":
          a=0
        else:    
          raise AssertionError
      except:
        print("Please enter a valid input")
      
    if ans=="n":
        t=0


    

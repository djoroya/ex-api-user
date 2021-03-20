
import tools.ConnectDB as DB
import os

# Re-start DB
DB.startDB()


## new user 
UserName ='djoroya'
PC = '01477'

code_error = DB.communications(UserName,PC)

print("code error = ",code_error)
print("successful")


## add incorrect PC
UserName ='txi'
PC = '014770'

code_error = DB.communications(UserName,PC)

print("code error = ",code_error)
print("PC doesn''t exist")

## try add new same user  
UserName ='djoroya'
PC = '01477'

code_error = DB.communications(UserName,PC)

print("code error = ",code_error)
print("The user already exist ")






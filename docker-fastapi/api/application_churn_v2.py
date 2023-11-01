from datetime import datetime, timedelta
from typing import Union

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

import pandas as pd
import os
import joblib
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from enum import Enum



# openssl rand -hex 64
SECRET_KEY = "5a3ca8b20b6fb2966d895c227b19a8619a26048e40db22b082041a6fed16db9a655f188acdfe82b6b70e53ab06ffb4808abd1218df3f15eeaf29569b27953047"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


fake_users_db = {
    "alice": {
        "username": "alice",
        "hashed_password": "$2b$12$rQIkUlF8c952HFhq2dhCpucDhg5FPTjkt0vuAWih.s7veO60QclXW",
        "disabled": False,
    },
    "bob": {
        "username": "alice",
        "hashed_password": "$2b$12$pUJ/WREJcpthyGz7PfNGX.qeZxaK17UiLqV2J5p5EVlgW2EExdCb6",
        "disabled": False,
    },
    "clementine": {
        "username": "alice",
        "hashed_password": "$2b$12$y7HOHMz.ol.aEv/BnXZNi.U6CYAubfINed6ayGGenmgbpOpUKEP8K",
        "disabled": False,
    }
}


api = FastAPI()

### Système d'autentification
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class User(BaseModel):
    username: str
    disabled: Union[bool, None] = None


class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@api.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}




@api.get('/')
async def get_index(current_user: User = Depends(get_current_active_user)):
	"""returns greetings
    """
	return {
		'greetings':'welcome'
	}

## Api

## Fonction et classe

class Model_datascience(str, Enum):
	Randomforest="Randomforest"
	DecisionTreeClassifier="DecisionTreeClassifier"

class Yes_or_no(str, Enum):
	yes = "yes"
	no = "no"


class ModelMultipleLines(str, Enum):
	yes = "yes"
	no = "no"
	no_phone_service = "no phone service"
	



class ModeleInternetService(str, Enum):
	dsl = "dsl"
	fiber_optic="fiber optic"
	no = "no"

class ModeleContract(str, Enum):
	month_to_month = "month-to-month"
	one_year = "one year"
	two_year="two year"


class ModelePaymentMethod(str, Enum):
	bank_transfer="bank transfer (automatic)"
	credit_card="credit card (automatic)"
	electronic_check="electronic check"
	mailed_check="mailed check"

def yes_no(rep):
	return 1 if rep=='yes' else 0

def replace_val(rep,val):
	return 1 if rep==val else 0
	
## Chargement donné
df = pd.read_csv(os.path.join(os.getcwd(), "donne/df_test.csv"), header=0)


## Fonction api



@api.get('/')
async def get_index(current_user: User = Depends(get_current_active_user)):
	"""returns greetings
    """
	return {
		'greetings':'welcome'
	}



@api.post('/modelisation')
async def post_modelisation(Model:Model_datascience,SeniorCitizen:int,Partner:Yes_or_no,Dependents:Yes_or_no,tenure:int,
							PhoneService:Yes_or_no,OnlineSecurity:Yes_or_no,OnlineBackup:Yes_or_no,DeviceProtection:Yes_or_no,
							TechSupport:Yes_or_no, PaperlessBilling:Yes_or_no,MonthlyCharges:float,	PaymentMethod:ModelePaymentMethod, 
							Contract:ModeleContract,InternetService:ModeleInternetService,MultipleLines:ModelMultipleLines,
							current_user: User = Depends(get_current_active_user)):
	if SeniorCitizen not in [0,1]:
		raise HTTPException(status_code=422, detail="Valeur de SeniorCitizen doit être 1 ou 0")
	donne=[SeniorCitizen,yes_no(Partner),yes_no(Dependents),tenure,yes_no(PhoneService),yes_no(OnlineSecurity),yes_no(OnlineBackup),
			yes_no(DeviceProtection),yes_no(TechSupport),yes_no(PaperlessBilling),MonthlyCharges,
			replace_val(PaymentMethod,"bank transfer (automatic)"),replace_val(PaymentMethod,"credit card (automatic)"),
			replace_val(PaymentMethod,"electronic check"),replace_val(PaymentMethod,"mailed check"),replace_val(Contract,"month-to-month"),
			replace_val(Contract,"one year"),replace_val(Contract,"two year"),replace_val(InternetService,"dsl"),
			replace_val(InternetService,"fiber optic"),replace_val(InternetService,"no"),
			replace_val(MultipleLines,"no"),replace_val(MultipleLines,"no phone service"),replace_val(MultipleLines,"yes")
			]
	if Model=="Randomforest":
		modele = joblib.load(os.path.join(os.getcwd(), "models", "Randomforest_Model.pkl"))
	elif Model=="DecisionTreeClassifier":
		modele = joblib.load(os.path.join(os.getcwd(), "models", "DecisionTreeClassifier_Model.pkl"))
	classe_pred=modele.predict([donne])
	proba=modele.predict_proba([donne])
	if classe_pred[0]==1:
		res="Yes"
	elif classe_pred[0]==0:
		res="No"

	# return {"score":score,"proba":proba}
	return {"Churn":res,"Probabilité Churn No=":round(proba[0][0]*100,2),"Probabilité Churn Yes=":round(proba[0][1]*100,2)}


@api.get('/score')
def get_score(current_user: User = Depends(get_current_active_user)):
	modele_Randomforest = joblib.load(os.path.join(os.getcwd(), "models", "Randomforest_Model.pkl"))
	modele_DecisionTreeClassifier = joblib.load(os.path.join(os.getcwd(), "models", "DecisionTreeClassifier_Model.pkl"))
	y_test = df['Churn']
	X_test = df.drop(['Churn'], axis=1)
	y_pred_dtc=modele_DecisionTreeClassifier.predict(X_test)
	y_pred_RF=modele_Randomforest.predict(X_test)
	return {'Randomforest':{"score accuracy":round(modele_Randomforest.score(X_test, y_test)*100,2), 
								"score f1":round(f1_score(y_pred_RF, y_test,average='macro')*100,2),
								"score de precision":round(precision_score(y_pred_RF, y_test,average='macro')*100,2),
								"score de recall":round(recall_score(y_pred_RF, y_test,average='macro')*100,2)},
			'DecisionTreeClassifier':{"score accuracy":round(modele_DecisionTreeClassifier.score(X_test, y_test)*100,2), 
										"score f1":round(f1_score(y_pred_dtc, y_test,average='macro')*100,2),
										"score de precision":round(precision_score(y_pred_dtc, y_test,average='macro')*100,2),
										"score de recall":round(recall_score(y_pred_dtc, y_test,average='macro')*100,2)}
			
			}
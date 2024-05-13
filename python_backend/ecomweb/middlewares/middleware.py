from fastapi import Request,HTTPException
from jose import jwt,JWTError
from ecomweb.settings.setting import ALGORITHM,SECRET_KEY

ALGORITHMM = str(ALGORITHM)
SECRET_KEYY = str(SECRET_KEY)

async def authorize(request:Request,call_back):
    access_token = request.cookies.get("access_token")
    pathname = request.url.path
    print(access_token,"access_token",ALGORITHMM,"Algorithm",SECRET_KEYY,"secret kry")
    protected_urls = ["/addproduct"]
    if access_token:
        for protected_url in protected_urls:
            if protected_url == pathname:
                try:
                    payload = jwt.decode(access_token,SECRET_KEYY,algorithms=[ALGORITHMM])
                    print(payload)

                except JWTError:
                    raise HTTPException(status_code=401, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    response = await call_back(request)
    return response

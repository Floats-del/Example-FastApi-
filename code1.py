from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import db_tables.tables as tables
from db import engine
from routers import posts, users, auth, likes


#form docomenration of fastapi CORS
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(title="Social Network Aggregator API")

origins = [
    # 1. Vite (React, Vue, Svelte, Tailwind setups)
    "http://localhost:5173",
    "http://127.0.0.1:5173",

    # 2. Next.js, Create React App, and Node/Express frontends
    "http://localhost:3000",
    "http://127.0.0.1:3000",

    # 3. Nuxt.js, legacy Vue CLI, and general Webpack setups
    "http://localhost:8080",
    "http://127.0.0.1:8080",

    # 4. Angular default port
    "http://localhost:4200",
    "http://127.0.0.1:4200",

    # 5. Mobile App Emulators (If you build an iOS/Android app later)
    "http://10.0.2.2:8000",  # Android emulator loopback to your local machine

    # 6. Your Production Domains (When you deploy)
    "https://www.yourdomain.com",
    "https://yourdomain.com",
    "https://staging.yourdomain.com",
]


app.add_middleware(
    CORSMiddleware, #when req comes b4 it can hit any routes it comes to this function!
    allow_origins=origins, #which domains can talk to us, if we want public api we can =["*"]
    allow_credentials=True, 
    #so here is the deal with credentials: When a browser makes a request, it normally strips out things like HTTP 
        #cookies, TLS client certificates, or Authorization headers (like your JWT tokens) for security reasons unless 
            #explicitly told it's allowed. Setting allow_credentials=True tells the browser: "Yes, it is safe to send the
                #user's login tokens and cookies along with the cross-origin request.
                
    allow_methods=["*"], #this rn means all types of request get,post etc! but we can specify which kind of req v accepiting
    allow_headers=["*"], #same for headers
)




# Mount operational modular router components 
app.include_router(router=posts.router)
app.include_router(router=users.router)
app.include_router(router=auth.router)
app.include_router(router=likes.router)

@app.get("/", include_in_schema=False)
def home():
    """Redirects the index route base entry straight to Interactive OpenAPI documents."""
    return RedirectResponse(url="/docs")




#git lecture:
"""
1) we made .gitignore which holds the files we dont want pushed to githup
2) then we do pip list > requirements.txt -> since we cant import full venv we can the libs we used and theri versions ;)
3) this way if someone cloned our repo they can just pip install -r requirements.txt and boom
4) i went and signed in to github and created a new repo it gave me these commands:
echo "# Example-FastApi-" >> README.md 
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/Floats-del/Example-FastApi-.git
git push -u origin main

we dont want the readme so far in lecture so we
5) now ill be in virtual envirement dw, git init 
6) we will skip the add README.md rather we will do: git add --all -> we will get errors dw
6.5) if u do: git ls-files -> it tells us how many files are ready for commit to github
7) then to actaully push them to git we do: git commit -m "my first push of all files"
8) then we do: git branch -M main
9) then we do: git remote add origin https://github.com/Floats-del/Example-FastApi-.git -> stores on github our data


10) git add . -> tells github to add new changes to github! (btw ive successfully added my stuff yo gh currently till point(9))
11) then we make some changes like currently im wrtining this comment and then we do: 
    git commit -m "feat: added comment 10 and 11 lol just to see git's responce"
12) then git push origin main -> to actually upload on gh



13) well comment 10,11,12 are added to github repo all i had to do was ctrl+s -> git add . -> git commit -m "fix: actually added comments 10 and 11" -> git push origin main
    and done! we could also: git add filename -> for solo update 
14) now lets see rollback since atp i must have 2 versions of this code with 10,11,12 and without!
15) git log --oneline -> tells us sanpshot histry:
2795685 (HEAD -> main, origin/main) fix: actually added comments 10 and 11
6498506 feat: added comment 10 and 11 lol just to see git's responce
7fd7f7e my first push of all files
f5509b4 my first push of all files

these ids are just like revision numbers in alembic ;)
16) git checkout 7fd7f7e -> lets us check old version not fully rollback!
17) to comeback form old version checking we do: git checkout main
18) litral rollback: git revert 6498506  -> we can revert back but future changes snapshots exits!

19) git reset --hard 7fd7f7e -> rollsback and destrous future snapshotes!
20) to come back to latest snapshot we do: git checkout main 


21) git checkout HEAD~1 -> 1 step back 
22) git log --oneline --graph --all --decorate -> see all snapshots
23) git checkout <hash> -> goes to a specific snapshot!

24) delete file form dir and git:
git rm filename.py
git commit -m "remove filename.py"
git push


25) delete file form git but keep on dir:
git rm --cached filename.py
git commit -m "stop tracking filename.py"
git push

if its a folder do: git rm -r --cached name


points to be noted: (IMP)
If you haven't committed them: Git will warn you that you might lose those changes if you switch branches. You should either git commit them or git stash them first.
If you already committed them: You are safe! Since you made a commit, those changes are saved in the history, and you can switch back and forth freely.
"""

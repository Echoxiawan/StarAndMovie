from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
from User.models import User, Star
import requests
import os
import gc
import random
import time
import json
import sys

sys.path.append('...')

from recog import sourlab_face

sourlab_face.load_feature()
recog1 = sourlab_face(12)


def getFileType(filename):
  binfile = open(filename, 'rb') 
  ftype = 'unknown'
  binfile.seek(0) 
  first3 =tuple(binfile.read(3))
  if first3== (0xFF,0xD8,0xFF):
     ftype = 'jpg'
  else:
     binfile.seek(0) 
     first4 =tuple(binfile.read(4))
     if first4 == (0x89,0x50,0x4E,0x47):
       ftype = 'png'
  binfile.close()
  return ftype

@csrf_exempt
def starmovie(request):
    if request.method == 'POST':
        try:
            uname = request.POST['user']
            upic = request.FILES.get('upfile')
            fileName = str(int(round(time.time() * 1000))) + str(random.randint(1, 100))

            f = open(os.path.join('...', fileName), 'wb')
            for chunk in upic.chunks():
                f.write(chunk)
            f.close()

            fileType = getFileType(os.path.join('...', fileName))
            if fileType == 'unknown':
                res = {"errorCode": 100, "errorMsg": "ImageFormatError"}
                return HttpResponse(json.dumps(res, ensure_ascii=False), content_type="application/json")
            else:
                os.rename(os.path.join('...', fileName), os.path.join('...', fileName + "." + fileType))
                fileName = fileName + "." + fileType

            feature = recog1.recognition(os.path.join('...', fileName))
            print(feature)
            if isinstance(feature, int):
                if(feature == -1):
                  res = {"errorCode": -1, "errorMsg": "detect no fase"}
                  return HttpResponse(json.dumps(res), content_type="application/json")
                else:
                  res = {"errorCode": 0, "errorMsg": "detect more than 2 faces"}
                  return HttpResponse(json.dumps(res), content_type="application/json")
            else:
                sname, similarity, simg_path = recog1.find_nearest(feature)
                similarity = round(similarity, 2)
                print(similarity)

                try:
                  user = User.objects.get(username=uname)
                  user.userpic = os.path.join('', fileName)
                  user.starname = sname
                  user.starpic = simg_path
                  user.similarity = similarity
                  user.save()
                except User.DoesNotExist:
                  newuser = User(username=uname, starname=sname, userpic=os.path.join('...', fileName),
                               starpic=simg_path, similarity=similarity)
                  newuser.save()

                finally:
                  star = Star.objects.get(starname=sname)
                  moviedes = star.description
                  moviename = star.moviename
                  print(sname)
                  print(simg_path)
                  print(moviedes)
                  print(moviename)
                  res = {
                    "errorCode": 1,
                    "errorMsg": "success",
                    "similarity": similarity,
                    "starname": sname,
                    "starpic": simg_path,
                    "moviename": moviename,
                    "moviedes": moviedes,
                  }
                  return HttpResponse(json.dumps(res), content_type="application/json")

        except Exception as e:
            res = {"errorCode": -5, "errorMsg": "uploadfail"}
            return HttpResponse(json.dumps(res), content_type="application/json")

    return HttpResponse('requestfail')

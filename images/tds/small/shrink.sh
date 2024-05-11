cp ../*.jpg .
mogrify -auto-orient -thumbnail 300x *.jpg

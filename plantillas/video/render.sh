set -e
D=(0 4.0 3.6 3.6 3.6 4.4 4.0)
for i in 1 2 3 4 5 6; do
 d=${D[$i]}; fo=$(python3 -c "print($d-0.35)")
 ffmpeg -y -loglevel error -framerate 30 -i bg$i.png -framerate 30 -i gbig.png -framerate 30 -i gsmall.png -filter_complex "\
[0]loop=-1:1,setpts=N/30/TB,trim=duration=$d,format=yuv420p[b];\
[1]loop=-1:1,setpts=N/30/TB,trim=duration=$d,format=rgba,rotate=a=t*0.35:c=none[g1];\
[2]loop=-1:1,setpts=N/30/TB,trim=duration=$d,format=rgba,rotate=a=-t*0.9:c=none[g2];\
[b][g1]overlay=x=600:y=1560[t1];[t1][g2]overlay=x=780:y=120,format=yuv420p,fade=in:st=0:d=0.35,fade=out:st=$fo:d=0.35[v]" \
 -map "[v]" -r 30 -c:v libx264 -crf 20 -preset veryfast -pix_fmt yuv420p -t $d tmp_s$i.mp4 && mv tmp_s$i.mp4 s$i.mp4
done
printf "file 's%d.mp4'\n" 1 2 3 4 5 6 > list.txt
ffmpeg -y -loglevel error -f concat -safe 0 -i list.txt -c copy tmp_v.mp4
ffmpeg -y -loglevel error -i tmp_v.mp4 -f lavfi -i anullsrc=r=44100:cl=stereo -map 0:v -map 1:a -c:v copy -c:a aac -b:a 64k -shortest -movflags +faststart tmp_final.mp4 && mv tmp_final.mp4 mecanica_reel.mp4

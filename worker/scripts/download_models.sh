if [ -f "checkpoints/20180402-114759-vggface2.pt" ]; then
  echo "20180402-114759-vggface2.pt exists"
else
  echo "downloading 20180402-114759-vggface2.pt"
  curl https://github.com/timesler/facenet-pytorch/releases/download/v2.2.9/20180402-114759-vggface2.pt --output ./checkpoints/20180402-114759-vggface2.pt
fi
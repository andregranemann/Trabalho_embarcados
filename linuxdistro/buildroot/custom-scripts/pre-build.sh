#!/bin/sh
  
  cp $BASE_DIR/../custom-scripts/S41network-config $BASE_DIR/target/etc/init.d
  chmod +x $BASE_DIR/target/etc/init.d/S41network-config
  cp $BASE_DIR/../custom-scripts/trabalho1.py $BASE_DIR/target/usr/bin
  chmod +x $BASE_DIR/target/usr/bin/trabalho1.py
  cp $BASE_DIR/../custom-scripts/S42server.sh $BASE_DIR/target/etc/init.d
  chmod +x $BASE_DIR/target/etc/init.d/S42server.sh

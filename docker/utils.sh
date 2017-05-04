#!/bin/bash

release () {
  # returns the operating system major release
  if [ -f /etc/redhat-release ]; then
    rel="el$(cat /etc/redhat-release | grep -o -E '[0-9]+' | head -1 | sed -e 's/^0\+//')"
  else
    rel="cflinuxfs2"
  fi
  echo "${rel}"
}

cpu () {
  # returns the operating system cpu type
  echo $(uname -m)
}

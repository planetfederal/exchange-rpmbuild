# exchange-rpmbuild

### build process

```bash
vagrant up
vagrant ssh
QA_RPATHS=$[ 0x0001|0x0010 ] rpmbuild --define '_topdir /vagrant' \
                                      --define 'git_url https://MYUSERNAME:MYPASSWORD@github.com/boundlessgeo/exchange.git' \
                                      -bb /vagrant/SPECS/el6/exchange.spec
```

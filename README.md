# exchange-rpmbuild

### build process

```bash
vagrant up
vagrant ssh
QA_RPATHS=$[ 0x0001|0x0010 ] rpmbuild --define '_topdir /vagrant' \
                                      --define 'git_user add_username' \
                                      --define 'git_password add_password' \
                                      -bb /vagrant/SPECS/el6/exchange.spec
```

#!/usr/bin/env python

import os, sys, getopt

TESTNAME="identityref"

# generate bindings in this folder

def main():
  try:
    opts, args = getopt.getopt(sys.argv[1:], "k", ["keepfiles"])
  except getopt.GetoptError as e:
    print str(e)
    sys.exit(127)

  k = False
  for o, a in opts:
    if o in ["-k", "--keepfiles"]:
      k = True

  this_dir = os.path.dirname(os.path.realpath(__file__))
  os.system("/usr/local/bin/pyang \
            --plugindir /Users/rjs/Code/pyangbind/btplugin \
            -p %s -f bt \
            -o %s/bindings.py %s/%s.yang" % (this_dir, this_dir, this_dir, TESTNAME))

  from bindings import identityref

  i = identityref()

  for j in ["id1", "idr1"]:
    assert hasattr(i.test_container, j), "%s leaf does not exist in the container" % i

  assert i.test_container.id1 == "", "id1 leaf had an unexpected value (%s)" % i.test_container.id1
  assert i.test_container.idr1 == "", "idr1 leaf had an unexpected value (%s)" % i.test_container.idr1

  passed = True
  try:
    i.test_container.id1 = "hello"
  except:
    passed = False
  assert passed == False, "id1 leaf set to invalid value"

  for k in ["option-one", "option-two"]:
    passed = True
    try:
      i.test_container.id1 = k
    except:
      passed = False
    assert passed == True, "id1 leaf was set to an invalid value (%s)" % k

  # checks that the namespaces are right
  for k in ["remote-one", "remote-two"]:
    passed = True
    try:
      i.test_container.idr1 = k
    except:
      passed = False
    assert passed == True, "idr1 leaf was set to an invalid value (%s)" % k


  if not k:
    os.system("/bin/rm %s/bindings.py" % this_dir)
    os.system("/bin/rm %s/bindings.pyc" % this_dir)

if __name__ == '__main__':
  main()
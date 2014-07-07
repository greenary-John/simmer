import sys
import os
import ConfigParser
import optparse

#-----------------------------------------------------
CMD_OPT_SECTION = "CmdLineOpts"
CMD_ARG_SECTION = "CmdLineArgs"

'''
A ConfigManager combines options specified on the command line with those specified in
a config file.
The parameter, opConfig, is a callable that accepts an instance of optparse.OptionParser; it adds whatever options it wants to the parser, except:
	-c --config	To specify a config file.
	-D --define	To define/override a config parameter.
'''
class ConfigManager(object):
    def __init__(self, configureOP):
        self.cp=SimmerConfigParser()
        self.op=optparse.OptionParser()

	#
	self.op.add_option("-c", "--config", dest="configFiles", default=[], 
	    action="append",
	    metavar="FILE",
	    help="Specify a config file. This option can be repeated to specify more than one config file; they will be read in order (last setter wins). If (and only if) no config files are specified, the default config file.")

	#
	self.op.add_option("-D", "--define", dest="defs", default=[],
	    action="append",
	    metavar="section.variable=value",
	    help="Define or override a config setting.")

	#
	configureOP(self.op)

    def defaultConfigFile(self):
	return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "config.cfg"))

    def readConfig(self, argv=None):
	# First, parse the command line
	if argv is None:
	    argv=sys.argv
	(opts,args) = self.op.parse_args(argv)

	# Find read config files
	if len(opts.configFiles) == 0:
	    opts.configFiles.append(self.defaultConfigFile())
	self.cp.read(opts.configFiles)

	# Inject command line opts into config 
	if not self.cp.has_section(CMD_OPT_SECTION):
	    self.cp.add_section(CMD_OPT_SECTION)
	if not self.cp.has_section(CMD_ARG_SECTION):
	    self.cp.add_section(CMD_ARG_SECTION)
	for (n,v) in opts.__dict__.items():
	    self.cp.set(CMD_OPT_SECTION, n, v)
	self.cp.set(CMD_ARG_SECTION,"args",args)

	# Inject "-D" command line opts into config
	for dv in opts.defs:
	    parts = dv.split("=",1)
	    n = parts[0]
	    value = parts[1] if len(parts)==2 else None
	    parts = n.split(".", 1)
	    if len(parts) == 2:
	        section,varname = parts
	    else:
		section = CMD_OPT_SECTION
	        varname = n
	    self.cp.set(section, varname, value)

	return self.cp

#-----------------------------------------------------
'''
A SimmerConfigParser is a subclass of SafeConfigParser that adds a couple of useful methods:
	sectionsWith : returns a list of section names where the section contains a given variable
	getConfigObj : returns all the vars in a section in a dictionary
In addtion, a SimmerConfigParser has case sensitive option names.
'''
class SimmerConfigParser(ConfigParser.ConfigParser):
    # override default: make names case sensitive
    def optionxform(self, name):
        return name

    def has_own_option(self, section, name):
        if self.has_option(section,name):
	    if self.has_option('DEFAULT',name) \
	    and self.get(section,name,True) == self.get('DEFAULT',name,True):
		return False
	    else:
	        return True
	else:
	    return False

    def own_options(self, section):
        return filter( lambda o:self.has_own_option(section, o), self.options(section) )

    def own_items(self, section):
        return filter( lambda i:self.has_own_option(section, i[0]), self.items(section) )

    # returns list of section names where section contains the given var name
    # and (optionally) that var has the given value
    def sectionsWith(self,name,value=None):
        rlist=[]
        for s in self.sections():
            for (var,val) in self.items(s):
                if var==self.optionxform(name) and (value==None or val==value):
                    rlist.append(s)
        return rlist

    # returns a dict containing all the vars in a section. If no section named, returns
    # all vars from all sections as a 2-level dict.
    def getConfigObj(self,section=None):
	if section:
	    return dict(self.own_items(section))
        sectionInfo={}
        for s in self.sections():
	    sectionInfo[s] = dict(self.own_items(s))
        return sectionInfo

def __testSimmerConfigParser__():
    import StringIO

    s='''

[DEFAULT]
inheritMe=howdy

[SectionOne]
foo=10
bar=%(foo)s
inheritMe=hello

[SectionTwo]
foo=99
'''
    scp = SimmerConfigParser()
    scp.readfp(StringIO.StringIO(s))

    print scp.sectionsWith("foo")
    print scp.sectionsWith("FOO")
    print scp.sectionsWith("foo","10")
    print scp.sectionsWith("bar","10")
    print scp.sectionsWith("inheritMe")
    print scp.sectionsWith("inheritMe","howdy")
    print scp.getConfigObj('SectionOne')
    print scp.getConfigObj()

def __testConfigManager__():
    def setConfigOptions(op):
	op.add_option("-n", "--number", metavar="NUM", dest="n", type="int", help="A number.")
        
    argv=["-n","99", "-D", "SectionOne.bar=xyzzy","-D","newvar=17","arg1","arg2","arg3"]
    cm = ConfigManager(setConfigOptions)
    c = cm.readConfig()
    print c.sections()
    global cp
    cp = c


def __test__():
    __testSimmerConfigParser__()
    __testConfigManager__()

if __name__=="__main__":
    __test__()

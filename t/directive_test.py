from template import Template
from template.test import TestCase, main


class DirectiveTest(TestCase):
  def testDirectives(self):
    ttobjs = (('tt', Template()),
              ('pre', Template({ 'PRE_CHOMP': 1 })),
              ('post', Template({ 'POST_CHOMP': 1 })),
              ('trim', Template({ 'INCLUDE_PATH': 'test/lib', 'TRIM': 1 })))
    self.Expect(DATA, ttobjs, self._callsign())


DATA = r"""
#------------------------------------------------------------------------
# basic directives
#------------------------------------------------------------------------
-- test --
[% a %]
[%a%]
-- expect --
alpha
alpha

-- test --
pre [% a %]
pre[% a %]
-- expect --
pre alpha
prealpha

-- test --
[% a %] post
[% a %]post
-- expect --
alpha post
alphapost

-- test --
pre [% a %] post
pre[% a %]post
-- expect --
pre alpha post
prealphapost

-- test --
[% a %][%b%][% c %]
-- expect --
alphabravocharlie

-- test --
[% 
a %][%b
%][%
c
%][%
         d
%]
-- expect --
alphabravocharliedelta

#------------------------------------------------------------------------
# comments
#------------------------------------------------------------------------
-- test --
[%# this is a comment which should
    be ignored in totality
%]hello world
-- expect --
hello world

-- test -- 
[% # this is a one-line comment
   a
%]
-- expect --
alpha

-- test -- 
[% # this is a two-line comment
   a =
   # here's the next line
   b
-%]
[% a %]
-- expect --
bravo

-- test --
[% a = c   # this is a comment on the end of the line
   b = d   # so is this
-%]
a: [% a %]
b: [% b %]
-- expect --
a: charlie
b: delta

#------------------------------------------------------------------------
# manual chomping
#------------------------------------------------------------------------

-- test --
[% a %]
[% b %]
-- expect --
alpha
bravo

-- test --
[% a -%]
[% b %]
-- expect --
alphabravo

-- test --
[% a -%]
     [% b %]
-- expect --
alpha     bravo

-- test --
[% a %]
[%- b %]
-- expect --
alphabravo

-- test --
[% a %]
     [%- b %]
-- expect --
alphabravo

-- test --
start
[% a %]
[% b %]
end
-- expect --
start
alpha
bravo
end

-- test --
start
[%- a %]
[% b -%]
end
-- expect --
startalpha
bravoend

-- test --
start
[%- a -%]
[% b -%]
end
-- expect --
startalphabravoend

-- test --
start
[%- a %]
[%- b -%]
end
-- expect --
startalphabravoend

#------------------------------------------------------------------------
# PRE_CHOMP enabled 
#------------------------------------------------------------------------

-- test --
-- use pre --
start
[% a %]
mid
[% b %]
end
-- expect --
startalpha
midbravo
end

-- test --
start
     [% a %]
mid
	[% b %]
end
-- expect --
startalpha
midbravo
end

-- test --
start
[%+ a %]
mid
[% b %]
end
-- expect --
start
alpha
midbravo
end

-- test --
start
   [%+ a %]
mid
[% b %]
end
-- expect --
start
   alpha
midbravo
end

-- test --
start
   [%- a %]
mid
   [%- b %]
end
-- expect --
startalpha
midbravo
end

#------------------------------------------------------------------------
# POST_CHOMP enabled 
#------------------------------------------------------------------------

-- test --
-- use post --
start
[% a %]
mid
[% b %]
end
-- expect --
start
alphamid
bravoend

-- test --
start
     [% a %]
mid
	[% b %]        
end
-- expect --
start
     alphamid
	bravoend

-- test --
start
[% a +%]
mid
[% b %]
end
-- expect --
start
alpha
mid
bravoend

-- test --
start
[% a +%]   
[% b +%]
end
-- expect --
start
alpha   
bravo
end

-- test --
start
[% a -%]
mid
[% b -%]
end
-- expect --
start
alphamid
bravoend


#------------------------------------------------------------------------
# TRIM enabled
#------------------------------------------------------------------------
-- test --
-- use trim --

[% INCLUDE trimme %]


-- expect --
I am a template element file which will get TRIMmed


-- test --
[% BLOCK foo %]

this is block foo

[% END -%]

[% BLOCK bar %]

this is block bar

[% END %]

[% INCLUDE foo %]
[% INCLUDE bar %]
end
-- expect --
this is block foo
this is block bar
end


-- test --
<foo>[% PROCESS foo %]</foo>
<bar>[% PROCESS bar %]</bar>
[% BLOCK foo %]

this is block foo

[% END -%]
[% BLOCK bar %]

this is block bar

[% END -%]
end
-- expect --
<foo>this is block foo</foo>
<bar>this is block bar</bar>
end


-- test --
[% r; r = s; "-"; r %].
-- expect --
romeo-sierra.

-- test --
[% IF a; b; ELSIF c; d; ELSE; s; END %]
-- expect --
bravo

"""

main()

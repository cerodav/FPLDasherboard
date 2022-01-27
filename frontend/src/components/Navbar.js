import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { animated, useSpring } from 'react-spring';
import { useLockBodyScroll } from 'react-use';
import { ALLOW_DARK_MODE_TOGGLE, DEFAULT_REDIRECT } from '../constants'

function Navbar({darkMode}) {

    const [expand, setExpand] = useState(false);
    useLockBodyScroll(expand);
    const [navbarStyleProp, set, _] = useSpring(() => ({opacity: 1}));
    set({opacity: 1});

    return (
        <animated.div className="Navbar" style={navbarStyleProp}>
            <div className="navbar-left">
            </div>

            <div className="navbar-middle">
                <Link to={ DEFAULT_REDIRECT } onClick={ ALLOW_DARK_MODE_TOGGLE ? darkMode.toggle : ()=>{}}>
                    FPL<br/><span>DASHER</span><br/>BOARD
                </Link>
            </div>

            <div className="navbar-right">
            </div>

        </animated.div>
    );
}

export default Navbar;
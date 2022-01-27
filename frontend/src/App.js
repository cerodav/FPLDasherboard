import { DEFAULT_REDIRECT } from './constants';
import Navbar from './components/Navbar';
import React, { lazy, Suspense } from 'react';
import { Redirect, Route, Switch, useLocation } from 'react-router-dom';
import useDarkMode from 'use-dark-mode';
import './App.scss';
import './Bootstrap.scss';

// All pages are declared here
const ClassicLeagueHome = lazy(() => import('./components/ClassicLeagueHome'));

// All routes are declared here
const pages = [
  {
    pageLink: '/classicleague/*',
    view: ClassicLeagueHome,
    displayName: 'Live Classic League',
    showInNavbar: true,
  },
];

const App = () => {  
  const darkMode = useDarkMode(true);
  const location = useLocation();
  return (
    <div className="App">
      <Navbar {...{darkMode}}/>
      <Suspense fallback={<div/>}>
        <Switch location={location}>
          {/* {pages.map((page, index) => {
            return (
              <Route
                exact
                path={page.pageLink}
                render={({match}) => <page.view/>}
                key={index}
              />
            );
          })} */}
          <ClassicLeagueHome/>
          {/* <Redirect to={DEFAULT_REDIRECT} /> */}
        </Switch>
      </Suspense>
    </div>
  );
};

export default App;

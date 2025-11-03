// import { Application } from "express";
// import passport from "passport";
// import PassportConfig from "./PassportConfig";

// import localStrategy from "./passportStrategies/localStrategy";
// import passportGitHubStrategy from "./passportStrategies/githubStrategy";

// // No need to actually pass the instance of passport since it returns a singleton
// const passportConfig = new PassportConfig();
// passportConfig.addStrategies([localStrategy /* passportGitHubStrategy */]);
// const passportMiddleware = (app: Application): void => {
//   app.use(passport.initialize());
//   app.use(passport.session());
// };

// export default passportMiddleware;





// // passportMiddleware.ts
// import passport from 'passport';
// import PassportConfig  from './PassportConfig';
// import githubStrategy, { githubUsers } from './passportStrategies/githubStrategy';

// // Initialize strategies
// new PassportConfig([githubStrategy]);

// // Session serialization
// passport.serializeUser((user: any, done) => {
//   done(null, user.id); // Store user ID in session
// });

// passport.deserializeUser((id: number, done) => {
//   const user = githubUsers.find(u => u.id === id);
//   done(null, user || null);
// });

// export default passport;

// middleware/passportMiddleware.ts
import passport from 'passport';
import PassportConfig from './PassportConfig';
import githubStrategy, { githubUsers } from './passportStrategies/githubStrategy';

// Register GitHub strategy
new PassportConfig([githubStrategy]);

// Serialize user into session
passport.serializeUser((user: any, done) => {
  done(null, user.id); // store user ID
});

// Deserialize user from session
passport.deserializeUser((id: number, done) => {
  const user = githubUsers.find(u => u.id === id);
  done(null, user || null);
});

export default passport;

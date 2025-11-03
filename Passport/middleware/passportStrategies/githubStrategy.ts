// import { Strategy as GitHubStrategy, Profile } from 'passport-github2';
// import { PassportStrategy } from '../../interfaces/index';
// import { Request } from 'express';
// const githubStrategy: GitHubStrategy = new GitHubStrategy(
//     {
//         clientID: process.env.GITHUB_CLIENT_ID!,
//         clientSecret: process.env.GITHUB_CLIENT_SECRET!,
//         callbackURL: process.env.GITHUB_CALLBACK_URL!,
//         passReqToCallback: true,
//     },
    
//     async (req: Request, accessToken: string, refreshToken: string, profile: Profile, done: (err: any, user?: any) => void) => {
//         try {
//             // Minimal user object from GitHub profile
//             const user = { id: profile.id, name: profile.username || profile.displayName || 'No Name' };
//             return done(null, user);
//         } catch (err) {
//             return done(err as any);
//         }
//     },
// );

// const passportGitHubStrategy: PassportStrategy = {
//     name: 'github',
//     strategy: githubStrategy,
// };

// export default passportGitHubStrategy;



import { Strategy as GitHubStrategy, Profile } from "passport-github2";
import { PassportStrategy } from "../../interfaces";
import { Request } from "express";
import dotenv from "dotenv";
dotenv.config();

// simple in-memory user list
export const githubUsers: any[] = [];

const githubStrategy = new GitHubStrategy(
  {
    clientID: process.env.GITHUB_CLIENT_ID!,
    clientSecret: process.env.GITHUB_CLIENT_SECRET!,
    callbackURL: process.env.GITHUB_CALLBACK_URL!,
    passReqToCallback: true,
  },
  async (
    req: Request,
    accessToken: string,
    refreshToken: string,
    profile: Profile,
    done: (err: any, user?: any) => void
  ) => {
    try {
      // check if user already exists
      let user = githubUsers.find((u) => u.githubId === profile.id);

      // create new user if first login
      if (!user) {
        user = {
          id: githubUsers.length + 1,
          githubId: profile.id,
          name: profile.displayName || profile.username || "No Name",
          avatar: profile.photos?.[0]?.value || null,
        };
        githubUsers.push(user);
      }

      return done(null, user);
    } catch (err) {
      return done(err);
    }
  }
);

const passportGitHubStrategy: PassportStrategy = {
  name: "github",
  strategy: githubStrategy,
};


// ✅ Default export for the strategy itself
export default passportGitHubStrategy;

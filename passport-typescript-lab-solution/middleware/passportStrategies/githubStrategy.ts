import passport from "passport";
import { Request } from 'express';
import { Strategy as GitHubStrategy } from 'passport-github2';
import { PassportStrategy } from '../../interfaces/index';
import { database, userModel } from "../../models/userModel";


const githubStrategy: GitHubStrategy = new GitHubStrategy(
    {
        clientID: process.env.GITHUB_CLIENT_ID ?? (() => { throw new Error('CLIENT_ID missing'); })(),
        clientSecret: process.env.GITHUB_CLIENT_SECRET ?? (() => { throw new Error('CLIENTSECRET missing'); })(),
        callbackURL: "http://localhost:8000/auth/github/callback",
        passReqToCallback: true,
    },

    async (req: Request,
        accessToken: string,
        refreshToken: string,
        profile: any,
        done: (err?: Error | null, user?: Express.User, info?: object) => void) => {
        let user = null;
        try {
            user = userModel.findById(profile.id)
        } catch (error) {
            user = {
                id: parseInt(profile.id),
                name: profile.username,
            };
            database.push(user);
        }
        done(null, user);
    },
);

const passportGitHubStrategy: PassportStrategy = {
    name: 'github',
    strategy: githubStrategy,
};

passport.use(passportGitHubStrategy.name, passportGitHubStrategy.strategy);

export default passportGitHubStrategy;

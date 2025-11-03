// import express from "express";
// import expressLayouts from "express-ejs-layouts";
// import session from "express-session";
// import path from "path";
// import passportMiddleware from './middleware/passportMiddleware';

// const port = process.env.port || 8000;

// const app = express();

// app.set("view engine", "ejs");
// app.use(express.static(path.join(__dirname, "public")));
// app.use(
//   session({
//     secret: "secret",
//     resave: false,
//     saveUninitialized: false,
//     cookie: {
//       httpOnly: true,
//       secure: false,
//       maxAge: 24 * 60 * 60 * 1000,
//     },
//   })
// );

// import authRoute from "./routes/authRoute";
// import indexRoute from "./routes/indexRoute";

// import passport from "passport";



// // Middleware for express
// app.use(express.json());
// app.use(expressLayouts);

// app.use(express.urlencoded({ extended: true }));
// passportMiddleware(app);



// app.get('/auth/github',
//   passport.authenticate('github', { scope: [ 'user:email' ] }));

// app.get('/auth/github/callback', 
//   passport.authenticate('github', { failureRedirect: '/login' }),
//   function(req, res) {
//     // Successful authentication, redirect home.
//     res.redirect('/');
//   });

// app.use((req, res, next) => {
//   console.log(`User details are: `);
//   console.log(req.user);

//   console.log("Entire session object:");
//   console.log(req.session);

//   console.log(`Session details are: `);
//   console.log((req.session as any).passport);
//   next();
// });

// app.use("/", indexRoute);
// app.use("/auth", authRoute);

// app.listen(port, () => {
//   console.log(`🚀 Server has started on port ${port}`);
// });





























import express from "express";
import expressLayouts from "express-ejs-layouts";
import session from "express-session";
import path from "path";
import "dotenv/config";
import passport from "./middleware/passportMiddleware"; // ✅ Configured Passport instance

import authRoute from "./routes/authRoute";
import indexRoute from "./routes/indexRoute";

const port = process.env.PORT || 8000; // ✅ should be uppercase "PORT" to match .env
const app = express();

// -----------------------------
// 🔹 View Engine + Static Files
// -----------------------------
app.set("view engine", "ejs");
app.use(expressLayouts);
app.use(express.static(path.join(__dirname, "public")));

// -----------------------------
// 🔹 Session Middleware
// -----------------------------
app.use(
  session({
    secret: process.env.SESSION_SECRET || "secret",
    resave: false,
    saveUninitialized: false,
    cookie: {
      httpOnly: true,
      secure: false, // set to true only in production (HTTPS)
      maxAge: 24 * 60 * 60 * 1000, // 1 day
    },
  })
);

// -----------------------------
// 🔹 Initialize Passport
// -----------------------------
app.use(passport.initialize());
app.use(passport.session());

// -----------------------------
// 🔹 Express Middleware
// -----------------------------
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// -----------------------------
// 🔹 GitHub OAuth Routes
// -----------------------------
app.get(
  "/auth/github",
  passport.authenticate("github", { scope: ["user:email"] })
);

app.get(
  "/auth/github/callback",
  passport.authenticate("github", { failureRedirect: "/login" }),
  (req, res) => {
    // ✅ redirect to dashboard or home after successful login
    res.redirect("/dashboard");
  }
);

// -----------------------------
// 🔹 Debug Session and User
// -----------------------------
app.use((req, res, next) => {
  console.log("User details are:", req.user);
  console.log("Entire session object:", req.session);
  console.log("Session details are:", (req.session as any).passport);
  next();
});

// -----------------------------
// 🔹 Routes
// -----------------------------
app.use("/", indexRoute);
app.use("/auth", authRoute);

// -----------------------------
// 🔹 Start Server
// -----------------------------
app.listen(port, () => {
  console.log(`🚀 Server has started on port ${port}`);
});

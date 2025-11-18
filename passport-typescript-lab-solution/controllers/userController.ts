import { userModel } from "../models/userModel";

const getUserByEmailIdAndPassword = (email: string, password: string): Express.User => {
  const user = userModel.findOne(email);

  if (!user) {
    throw new Error(`Couldn't find user with email: ${email}`);
  }

  if (!isUserValid(user, password)) {
    throw new Error(`Password is incorrect for email: ${email}`);
  }

  return user;
};

const getUserById = (id: number): Express.User | null => {
  const user = userModel.findById(id);
  return user ?? null;
};

function isUserValid(user: any, password: string) {
  return user.password === password;
}

export {
  getUserByEmailIdAndPassword,
  getUserById,
};

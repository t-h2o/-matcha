import { OtherUserData, UserData } from './data-to-api/user';

export const emptyUser: UserData = {
  username: '',
  firstname: '',
  lastname: '',
  email: '',
  age: '',
  selectedGender: '',
  sexualPreference: '',
  bio: '',
  pictures: [],
  urlProfile: '',
  emailVerified: false,
  profile_complete: false,
  fameRating: 4,
};

export const emptyOtherUser: OtherUserData = {
  username: '',
  firstname: '',
  lastname: '',
  age: '',
  selectedGender: '',
  sexualPreference: '',
  bio: '',
  pictures: [],
  urlProfile: '',
  fameRating: 0,
  interests: [],
};

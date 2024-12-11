import { UserData } from './data-to-api/user';

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
  interests: [],
};

export const testUser: UserData = {
  username: 'testUser',
  firstname: 'test',
  lastname: 'user',
  email: 'test@test.com',
  age: '25',
  selectedGender: 'm',
  sexualPreference: 'e',
  bio: 'test bio',
  pictures: [],
  urlProfile: '',
  emailVerified: true,
  profile_complete: true,
  fameRating: 4,
  interests: [],
};

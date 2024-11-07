import { Component } from '@angular/core';
import { CardComponent } from '../UI/card/card.component';
import { chatContact } from '../shared/models/data-to-api/user';

const DummyChatContact: chatContact[] = [
  {
    username: 'JohnDoe',
    firstName: 'John',
    lastName: 'Doe',
    profilePicture: '/dummy-pics/placeholderPic.jpg'
  },
  {
    username: 'JaneDoe',
    firstName: 'Jane',
    lastName: 'Doe',
    profilePicture: '/dummy-pics/placeholderPic.jpg'
  },
  {
    username: 'Alice',
    firstName: 'Alice',
    lastName: 'Wonderland',
    profilePicture: '/dummy-pics/placeholderPic.jpg'
  },
  {
    username: 'Bob',
    firstName: 'Bob',
    lastName: 'Builder',
    profilePicture: '/dummy-pics/placeholderPic.jpg'
  },
  {
    username: 'Charlie',
    firstName: 'Charlie',
    lastName: 'Chaplin',
    profilePicture: '/dummy-pics/placeholderPic.jpg'
  },
];

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [CardComponent],
  templateUrl: './chat.component.html',
  styleUrl: './chat.component.scss'
})
export class ChatComponent {
  contacts: chatContact[] = DummyChatContact;
 
}

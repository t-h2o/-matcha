import { Component } from '@angular/core';
import { CustomButtonComponent } from '../../UI/custom-button/custom-button.component';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-login-form',
  standalone: true,
  imports: [CustomButtonComponent, FormsModule],
  templateUrl: './login-form.component.html',
  styleUrl: './login-form.component.scss'
})
export class LoginFormComponent {

}

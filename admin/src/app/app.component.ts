import { Component, OnInit, Inject } from '@angular/core';
import { DOCUMENT } from '@angular/common';
import { MatSnackBar } from '@angular/material/snack-bar';
import { UserErrorService } from './user-error.service'
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'Admin Console';

  constructor(
    private userError: UserErrorService,
    private snackBar: MatSnackBar,
    @Inject(DOCUMENT) private document: Document) {}

  ngOnInit(): void {
    this.userError.error.subscribe(message => {
      let action = 'dismiss';
      this.snackBar.open(message, action, {
        duration: 10000,
      });
    });
  }

  logout(): void {
    this.document.location.href = environment.apiLogout;
  }
}

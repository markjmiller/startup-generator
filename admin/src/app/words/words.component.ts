import { Component, OnInit } from '@angular/core';
import { WordsService } from '../words.service';

@Component({
  selector: 'app-words',
  templateUrl: './words.component.html',
  styleUrls: ['./words.component.css']
})
export class WordsComponent implements OnInit {

  constructor(private wordService: WordsService) { }

  ngOnInit(): void { }

  get canUndo() {
    return this.wordService.canUndo;
  }

  undo() {
    if (!this.canUndo) { return; }
    this.wordService.undo();
  }
}

import { Component, OnInit, Input, ViewChild, AfterViewInit } from '@angular/core';
import { Word, WordsService } from '../words.service';
import { MatFormField } from '@angular/material/form-field';

import { COMMA, ENTER } from '@angular/cdk/keycodes';
import { MatChipInputEvent } from '@angular/material/chips';

@Component({
  selector: 'app-words-list',
  templateUrl: './words-list.component.html',
  styleUrls: ['./words-list.component.css']
})
export class WordsListComponent implements OnInit, AfterViewInit {

  @ViewChild('wordForm') form: MatFormField;

  @Input() set_index: number;
  words: readonly Word[] = [];

  visible = true;
  selectable = true;
  removable = true;
  addOnBlur = true;
  readonly separatorKeysCodes: number[] = [ENTER, COMMA];

  searchValue: string;

  constructor(private wordService: WordsService) { }

  ngOnInit(): void {
    this.wordService.words(this.set_index)
      .subscribe(words => this.words = words);
  }

  ngAfterViewInit(): void {
    this.form.underlineRef.nativeElement.remove();
  }

  onInputChange(searchValue: string): void {  
    this.searchValue = searchValue;
  }

  add(event: MatChipInputEvent): void {
    this.searchValue = '';

    const input = event.input;
    const value = event.value;

    if ((value || '').trim()) {
      this.wordService.add({ word: value.trim(), set_index: this.set_index });
    }

    // Reset the input value
    if (input) {
      input.value = '';
    }
  }

  remove(word: Word): void {
    this.searchValue = '';

    if (this.words.indexOf(word) >= 0) {
      this.wordService.delete(word, this.set_index);
    }
  }
}

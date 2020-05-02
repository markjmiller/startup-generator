import { Component, OnInit, AfterViewInit } from '@angular/core';
import { Suggestion, SuggestionService, WordShuffler } from '../suggestion.service';

@Component({
  selector: 'app-suggestion',
  templateUrl: './suggestion.component.html',
  styleUrls: ['./suggestion.component.css']
})
export class SuggestionComponent implements OnInit {

  loading: boolean;
  firstWord: string;
  secondWord: string;
  shuffler: WordShuffler;
  
  constructor(private suggestion: SuggestionService) {
    this.loading = true;
    this.shuffler = new WordShuffler(this.suggestion, 2, 3);
  }

  ngOnInit(): void {
    this.requestNewSuggestion();
  }

  get tweetURL(): string {
    const text = `${ this.firstWord } for ${ this.secondWord }`;
    return ""; // Insert twitter api here
  }

  requestNewSuggestion(): void {
    this.loading = true;
    this.shuffler.get().subscribe(
      (data: Suggestion) => {
        this.loading = false;
        this.firstWord = data.word_1;
        this.secondWord = data.word_2;
      }
    );
  }
}

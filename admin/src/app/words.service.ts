import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import { map, finalize } from 'rxjs/operators';

import { environment } from './../environments/environment';

import { UserErrorService } from './user-error.service';

export interface Word {
  _id: string;
  word: string;
}

export interface WordRequest {
  word: string;
  set_index: number;
}

enum DocumentState {
  Set = 0,
  Pending,
  Failed
}

interface Document {
  _id: string;
  set_index: number;
  word: string;
  state: DocumentState;
}

interface SchemaDocument {
  _id: string;
  set_index: number;
  word: string;
}

interface SchemaWords {
  words: SchemaDocument[];
}

interface SchemaID {
  _id: string;
}

@Injectable({
  providedIn: 'root'
})
export class WordsService {

  private requestInProgress: boolean;
  private _words: BehaviorSubject<Document[]>;
  private undoAction = [];

  constructor(private http: HttpClient, private userError: UserErrorService) { }

  words(set_index: number): Observable<readonly Word[]> {
    if (this._words == null) {
      this._words = new BehaviorSubject<Document[]>([]);
      this.getWords();
    }
    return this._words
      .pipe(map(schemaArray =>
        schemaArray
         .filter(Document => Document.set_index === set_index)
         .map(Document => <Word>{ _id: Document._id, word: Document.word })));
  }

  private checkLoginError(error: HttpErrorResponse): void {
    if (error.status != environment.loginErrorCode) { return; }
    window.location.href = environment.apiLogin;
  }

  private getWords(): void {
    this.http.get<SchemaWords>(environment.apiAllWords)
      .subscribe(wordData =>
        this._words.next(wordData.words.map(x => <Document>{
          _id: x._id,
          word: x.word,
          set_index: x.set_index,
          state: DocumentState.Set
        })),
        (error: HttpErrorResponse) => {
          this.checkLoginError(error);
          console.log(`${error.status}: ${error.message}`);
          this.userError.show('Server error');
        }
      );
  }

  get canUndo(): boolean {
    return !this.requestInProgress && this.undoAction.length > 0;
  }

  undo(): void {
    if (!this.canUndo) { return; }
    const undoAction = this.undoAction.pop();
    undoAction();
  }

  add(newWord: WordRequest, noUndo?: boolean): void {
    if (this.requestInProgress) {
      this.userError.show('Waiting for server');
      return;
    }

    const currentWords = Array.from(this._words.value);

    if (this.findWord(currentWords, newWord.word, newWord.set_index)) {
      this.userError.show('Word already exists');
      return;
    }

    const document = <Document>{
      _id: null,
      set_index: newWord.set_index,
      word: newWord.word,
      state: DocumentState.Pending
    };

    this._words.next(
      Array.from(currentWords).concat(document)
    );

    this.requestInProgress = true;
    this.http.post<SchemaID>(environment.apiAdd, newWord)
      .pipe(finalize(() => this.requestInProgress = false))
      .subscribe(
        id => {
          const foundDocument = this._words.value.find(x => x._id === document._id);
          foundDocument._id = id._id;
          foundDocument.state = DocumentState.Set;
          if (!noUndo)
          {
            this.undoAction.push(() =>
              this.delete(<Word>{ _id: id._id, word: newWord.word }, newWord.set_index, true));
          }
        },
        (error: HttpErrorResponse) => {
          this.checkLoginError(error);
          console.log(`${error.status}: ${error.message}`);
          this.userError.show('Server error');
          document.state = DocumentState.Failed;
          this._words.next(currentWords);
        }
      );
  }

  delete(removeWord: Word, set_index: number, noUndo?: boolean): void {
    if (this.requestInProgress) {
      this.userError.show('Waiting for server');
      return;
    }

    const currentWords = Array.from(this._words.value);

    const docWord = this.findWord(currentWords, removeWord.word, set_index);
    if (!docWord)
    {
      this.userError.show(`"${docWord.word}" does not exists`);
      return;
    }

    if (docWord.state === DocumentState.Pending) {
      this.userError.show(`Cannot delete "${docWord.word}" yet`);
      return;
    }

    if (!docWord._id || docWord.state === DocumentState.Failed) {
      this.userError.show(`${docWord.word} was in a bad state.`);
    }

    if (!docWord._id) {
      this._words.next(
        currentWords.filter(word =>
          !(word.word === docWord.word && word.set_index === docWord.set_index))
      );
      return;
    }

    this._words.next(
      currentWords.filter(word => word._id !== docWord._id)
    );

    this.requestInProgress = true;
    this.http.delete(environment.apiDelete + '/' + docWord._id, { observe: 'response' })
      .pipe(finalize(() => this.requestInProgress = false))
      .subscribe(response => {
        if (response.status === 200) {
          this.userError.show(`"${docWord.word}" does not exists`);
          return;
        }
        if (!noUndo)
        {
          this.undoAction.push(() =>
            this.add(<WordRequest>{ word: removeWord.word, set_index: set_index }, true));
        }
      },
      (error: HttpErrorResponse) => {
        this.checkLoginError(error);
        console.log(`${error.status}: ${error.message}`);
        this.userError.show('Server error');
        this._words.next(currentWords);
      }
    );
  }

  private findWord(words: Document[], findWord: string, set_index: number) {
    return words.find(word => word.word === findWord && word.set_index === set_index);
  }
}

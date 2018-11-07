import React, { Component } from "react";
import logo from "./logo.svg";
import Title from "./components/Title.js";
import Options from "./components/Options.js";
import Documents from "./components/Documents.js";
import Grid from "@material-ui/core/Grid";
import "./App.css";

class App extends Component {
  constructor(props) {
    super(props);
    this.state = { documents: [] };

    this.updateDocuments = this.updateDocuments.bind(this);
  }

  updateDocuments(documents) {
    this.setState({ documents });
  }

  render() {
    return (
      <div className="App">
        <Grid container direction="column" spacing={24}>
          <Grid item>
            <Title />
          </Grid>
          <Grid item>
            <Grid
              container
              direction="row"
              spacing={24}
              alignItems="center"
              justify="center"
            >
              <Grid item xs={4}>
                <Options
                  documents={this.state.documents}
                  updateDocuments={this.updateDocuments}
                />
              </Grid>
              <Grid item xs={8}>
                <Documents documents={this.state.documents} />
              </Grid>
            </Grid>
          </Grid>
        </Grid>
      </div>
    );
  }
}

export default App;

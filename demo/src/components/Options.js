import React, { Component } from "react";
import Typography from "@material-ui/core/Typography";
import TextField from "@material-ui/core/TextField";
import { Slider } from "material-ui-slider";
import Grid from "@material-ui/core/Grid";
import axios from "axios";

class Options extends Component {
  constructor(props) {
    super(props);
    this.state = {
      entity: "",
      lowerSentiment: -1,
      upperSentiment: 1
    };

    this.search = this.search.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.handleSentimentChange = this.handleSentimentChange.bind(this);
  }

  search() {
    axios
      .get("/docs", {
        params: {
          entity: this.state.entity,
          lowerSentiment: this.state.lowerSentiment,
          upperSentiment: this.state.upperSentiment
        }
      })
      .then(r => this.props.updateDocuments(r.data))
      .catch(e => console.log(e));
  }

  handleChange = name => event => {
    this.setState({
      [name]: event.target.value
    });
  };

  handleSentimentChange(values) {
    this.setState({
      lowerSentiment: values[0] / 100,
      upperSentiment: values[1] / 100
    });
  }

  render() {
    return (
      <Grid
        container
        direction="column"
        spacing={24}
        alignItems="center"
        justify="center"
      >
        <form
          onSubmit={e => {
            e.preventDefault();
            this.search();
          }}
        >
          <Grid item>
            <TextField
              label="Entity"
              value={this.state.name}
              onChange={this.handleChange("entity")}
              margin="normal"
            />
          </Grid>
          <Grid item>
            <SentimentSlider
              lower={this.state.lowerSentiment}
              upper={this.state.upperSentiment}
              handleChange={this.handleSentimentChange}
            />
          </Grid>
        </form>
      </Grid>
    );
  }
}

class SentimentSlider extends Component {
  render() {
    return (
      <div>
        <Typography>Sentiment: </Typography>
        <Grid container direction="row" spacing={8}>
          <Grid item>
            <Typography>{this.props.lower}</Typography>
          </Grid>
          <Grid item>
            <Slider
              style={{ width: "200px" }}
              value={[this.props.lower * 100, this.props.upper * 100]}
              min={-100}
              max={100}
              onChangeComplete={this.props.handleChange}
              range
            />
          </Grid>
          <Grid item>
            <Typography>{this.props.upper}</Typography>
          </Grid>
        </Grid>
      </div>
    );
  }
}

export default Options;

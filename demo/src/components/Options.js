import React, { Component } from "react";
import TextField from "@material-ui/core/TextField";
import Button from "@material-ui/core/Button";
import CloudUploadIcon from "@material-ui/icons/CloudUpload";
import axios from "axios";

class ABSALoad extends Component {
  constructor(props) {
    super(props);
    this.fileInput = React.createRef();
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleSubmit(e) {
    e.preventDefault();
    if (!this.fileInput.current) {
      return;
    }

    let formData = new FormData();
    formData.append("file", this.fileInput.current.files[0]);
    axios
      .post("/absa/load", formData, {
        headers: {
          "Content-Type": "multipart/form-data"
        }
      })
      .catch(e => console.log(e));
  }

  render() {
    return (
      <form onSubmit={this.handleSubmit}>
        <input
          accept=".xml"
          id="contained-button-file"
          multiple
          type="file"
          style={{ display: "none" }}
          ref={this.fileInput}
        />
        <label htmlFor="contained-button-file">
          <Button variant="contained" color="default" component="span">
            Upload
            <CloudUploadIcon style={{ marginLeft: "0.25em" }} />
          </Button>
        </label>
        <Button
          variant="contained"
          color="default"
          component="span"
          onClick={this.handleSubmit}
        >
          Submit
        </Button>
      </form>
    );
  }
}

class ABSAQuery extends Component {
  constructor(props) {
    super(props);
    this.state = {
      query: ""
    };

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(e) {
    this.setState({ query: e.target.value });
  }

  handleSubmit(e) {
    e.preventDefault();
    const query = this.state.query;
    axios
      .get("/absa/query", { params: { query } })
      .then(r => this.props.updateResults({ entity: query, ...r.data }))
      .catch(e => console.log(e));
  }

  render() {
    return (
      <form onSubmit={this.handleSubmit}>
        <TextField
          label="Entity"
          value={this.state.query}
          onChange={this.handleChange}
          margin="normal"
        />
      </form>
    );
  }
}

class Options extends Component {
  render() {
    return (
      <div>
        <ABSALoad />
        <ABSAQuery updateResults={this.props.updateResults} />
      </div>
    );
  }
}

export default Options;

import React, { Component } from "react";
import Paper from "@material-ui/core/Paper";
import Typography from "@material-ui/core/Typography";

function Documents(props) {
  if (!Array.isArray(props.documents) || !props.documents.length) {
    return <Typography component="p"> Nothing to see here... </Typography>;
  }
  return props.documents.map(d => <Doc key={d.id} document={d} />);
}

class Doc extends Component {
  render() {
    return (
      <Paper elevation={1}>
        <Typography variant="h5" component="h5">
          {this.props.document.headline}
        </Typography>
        <Typography component="p">{this.props.document.content}</Typography>
        <Typography component="p">
          Main Entity: {this.props.document.entity}
        </Typography>
        <Typography component="p">
          Overall Sentiment: {this.props.document.sentiment}
        </Typography>
      </Paper>
    );
  }
}

export default Documents;

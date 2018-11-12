import React from "react";
import Typography from "@material-ui/core/Typography";
import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";

function Results(props) {
  const results = props.results;
  const scoreTitle = results.entity ? "Score: " : "";
  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between" }}>
        <Typography variant="h3" gutterBottom>
          {results.entity}
        </Typography>
        <Typography variant="h3" gutterBottom>
          {scoreTitle}
          {results.entity ? (results.score ? results.score : "?") : ""}
        </Typography>
      </div>
      {results.entries.map((e, i) => (
        <div key={i}>
          <Entry
            attribute={e.attribute}
            expression={e.expression}
            sentiment={e.sentiment}
          />
          <br />
        </div>
      ))}
    </div>
  );
}

function Entry(props) {
  return (
    <Card style={{ textAlign: "left" }}>
      <CardContent>
        <Typography variant="h5">{props.attribute}</Typography>
        <Typography>Sentiment: {props.sentiment}</Typography>
        <Typography>{props.expression}</Typography>
      </CardContent>
    </Card>
  );
}

export default Results;

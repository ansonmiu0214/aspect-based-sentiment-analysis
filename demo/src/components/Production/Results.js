import React, { Component } from "react";
import Typography from "@material-ui/core/Typography";
import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";
import ExpansionPanel from '@material-ui/core/ExpansionPanel';
import ExpansionPanelDetails from '@material-ui/core/ExpansionPanelDetails';
import ExpansionPanelSummary from '@material-ui/core/ExpansionPanelSummary';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import { withStyles } from "@material-ui/core";
import CardActions from '@material-ui/core/CardActions';
import Button from '@material-ui/core/Button';
import Grid from "@material-ui/core/Grid";
import DocumentModal from '../DocumentModal'

const panelStyle = theme => ({
  heading: {
    fontSize: theme.typography.pxToRem(20),
    flexBasis: '70%',
    flexGrow: 1,
  },
  numberHeading: {
    fontSize: theme.typography.pxToRem(20),
    color: theme.palette.text.secondary,
  }
});

function AttributePanel(props) {
  const { entry, handleChange, expanded, classes, dp, showDocument } = props
  const { attribute, score, entries } = entry 

  return (
    <ExpansionPanel expanded={expanded == attribute} onChange={handleChange(attribute)}>
      <ExpansionPanelSummary expandIcon={<ExpandMoreIcon />}>
        <Typography className={classes.heading}>{attribute}</Typography>
        <Typography className={classes.numberHeading} align="right">{Number(score).toFixed(dp)}</Typography>
      </ExpansionPanelSummary>
      <ExpansionPanelDetails>
        <Grid container spacing={24}>
          {entries.map(({ expression, sentiment, documentId }, idx) => 
            <Grid item xs={12}>
              <Card key={idx}>
                <CardContent>
                  <Grid container spacing={24}>
                    <Grid item xs={10} flexGrow>
                      <Typography color="textSecondary" gutterBottom>
                        Expression
                      </Typography>
                      <Typography>
                        {expression}
                      </Typography>
                    </Grid>
                    <Grid item xs={2}>
                      <Typography align="right" color="textSecondary" gutterBottom>
                        Sentiment
                      </Typography>
                      <Typography align="right">
                        {Number(sentiment).toFixed(dp)}
                      </Typography>
                    </Grid>
                  </Grid>
                </CardContent>
                <CardActions>
                  <Button size="small" onClick={event => showDocument(event, documentId)}>Document #{documentId}</Button>
                </CardActions>
              </Card>
            </Grid>
          )}
        </Grid>
      </ExpansionPanelDetails>
    </ExpansionPanel>
  )
}

const StyledPanel = withStyles(panelStyle)(AttributePanel)

class Results extends Component {
  constructor(props) {
    super(props)
    this.dp = 4
    this.handleChange = this.handleChange.bind(this)
    this.hideDocument = this.hideDocument.bind(this)
    this.showDocument = this.showDocument.bind(this)
  }

  state = {
    expanded: null,
    showDocument: null
  }

  handleChange = id => (event, expanded) => {
    this.setState({ expanded: expanded ? id : false })
  }

  hideDocument() {
    this.setState({ showDocument: null })
  }

  showDocument(event, documentId) {
    this.setState({ showDocument: documentId })
  }

  render() {
    const { results } = this.props;
    const { showDocument } = this.state
    const scoreTitle = results.entity ? "Score: " : "";
    return (
      <div>
        <div style={{ display: "flex", justifyContent: "space-between" }}>
          <Typography variant="h3" gutterBottom>
            {results.entity}
            {results.attribute ? ` - ${results.attribute}` : ""}
          </Typography>
          <Typography variant="h3" gutterBottom>
            {scoreTitle}
            {results.entity
              ? results.score !== null
                ? results.score.toFixed(this.dp)
                : "?"
              : ""}
          </Typography>
        </div>
        {results.entries.map(entry => 
          <StyledPanel 
            entry={entry} 
            dp={this.dp} 
            handleChange={this.handleChange} 
            expanded={this.state.expanded} 
            showDocument={this.showDocument} 
            />
        )}
        {
          (showDocument !== null) && <DocumentModal documentId={showDocument} api={"/absa/document"} handleClose={this.hideDocument} />
        }
      </div>
    );
  }
}

export default Results;

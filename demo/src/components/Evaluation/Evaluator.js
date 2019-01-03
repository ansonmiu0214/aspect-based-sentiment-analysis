import React, { Component } from "react";
import Heading from '../Heading'
import Loader from '../Loader'
import axios from 'axios'
import { Paper, Typography, Grid } from "@material-ui/core";
import { withStyles } from '@material-ui/core';
import ExpansionPanel from '@material-ui/core/ExpansionPanel';
import ExpansionPanelDetails from '@material-ui/core/ExpansionPanelDetails';
import ExpansionPanelSummary from '@material-ui/core/ExpansionPanelSummary';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import TagTable from "../TagTable";

const panelStyle = theme => ({
  heading: {
    fontSize: theme.typography.pxToRem(15),
    flexBasis: '33.33%',
    flexShrink: 0,
  },
  secondaryHeading: {
    fontSize: theme.typography.pxToRem(15),
    flexBasis: '10%',
    flexShrink: 0,
    color: theme.palette.text.secondary,
  },
  numberHeading: {
    fontSize: theme.typography.pxToRem(15),
    flexBasis: '20%',
    flexShrink: 0,
    color: theme.palette.text.secondary,
  }
});

function LabelledTagTable(props) {
  const { title, entities } = props
  return (
    <>
      <Typography variant="h5" component="h5" gutterBottom>
        {title}
      </Typography>
      <TagTable entities={entities}/>
    </>
  )
}

class Entry extends Component {
  constructor(props) {
    super(props)
    this.classes = props.classes
  }

  render() {
    const { breakdown, handleChange, expanded, classes, dp } = this.props
    const { id, score, ent_f1, attr_f1, model, truth } = breakdown
    return (
      <ExpansionPanel expanded={expanded === id} onChange={handleChange(id)}>
        <ExpansionPanelSummary expandIcon={<ExpandMoreIcon />}>
          <Typography className={classes.heading}>Document #{id}</Typography>
          <Typography className={classes.secondaryHeading}>Total F1 Score: {Number(score).toFixed(dp)}</Typography>
          <Typography className={classes.numberHeading}>Entity F1 Score: {Number(ent_f1).toFixed(dp)}</Typography>
          <Typography className={classes.numberHeading}>Attribute F1 Score: {Number(attr_f1).toFixed(dp)}</Typography>
        </ExpansionPanelSummary>
        <ExpansionPanelDetails>
          <Grid container spacing={24}>
            <Grid item xs={12} lg={6}>
              <LabelledTagTable title="Model Output" entities={model} />
            </Grid>
            <Grid item xs={12} lg={6}>
              <LabelledTagTable title="Ground Truth" entities={truth} />
            </Grid>
          </Grid>
        </ExpansionPanelDetails>
      </ExpansionPanel>
    )
  }
}

const StyledEntry = withStyles(panelStyle)(Entry)

class Breakdown extends Component {

  constructor(props) {
    super(props)
    this.handleChange = this.handleChange.bind(this)
  }

  state = {
    expanded: null
  }

  handleChange = id => (event, expanded) => {
    this.setState({ expanded: expanded ? id : false })
  }

  render() {
    const { breakdownList, dp } = this.props
    const { expanded } = this.state
    return (
      <div style={{width: '100%'}}>
        {
          breakdownList.map(breakdown => 
            <StyledEntry breakdown={breakdown} handleChange={this.handleChange} expanded={expanded} dp={dp} />  
          )
        }
      </div>
    )
  }

}

class Scores extends Component {
  
  constructor(props) {
    super(props)
  }

  render() {
    const { result, dp } = this.props
    return (
      <Paper style={{padding: '20px', marginBottom: '40px'}}>
        <Typography color="textSecondary" gutterBottom>
          Average F1 Score
        </Typography>
        <Typography variant="h3" component="h2" style={{marginBottom: '20px'}}>
          {Number(result).toFixed(dp)}
        </Typography>
      </Paper>
    )
  }
}

class Evaluator extends Component {

  constructor(props) {
    super(props)
    this.dp = 3
  }

  state = {
    result: null,
    breakdown: null,
    loading: true,
  }

  componentWillMount() {
    axios.get('/test')
      .then(({ data }) => {
        const { result, breakdown } = data
        this.setState({ loading: false, result: result, breakdown: breakdown })
      })
  }

  render() {
    const dp = this.dp
    const { result, breakdown, loading } = this.state
    return (
      <>
      <Heading text="Model Evaluation" />
      {loading && <Loader />}
      {!loading && 
        <>
        <Scores result={result} dp={dp}/>
        <Breakdown breakdownList={breakdown} dp={dp}/>
        </>
      }
      </>
    )

  }

}

export default Evaluator
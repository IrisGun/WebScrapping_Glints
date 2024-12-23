import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
import math
from datetime import datetime
import os


def create_charts(df):
    job_counts = df['category'].value_counts().reset_index()
    job_counts.columns = ['category', 'count']

    fig_job_counts = px.bar(job_counts, x='category', y='count', 
                            title='Job count by position',
                            labels={'category': 'Category of job position', 'count': 'Number of job post'},
                            color='category')
    fig_job_counts.update_layout(xaxis_tickangle=-45,height=600, width=1200)


    # Salary distribution by category
    fig_salary_distribution = px.box(df, x='category', y='standardize_salary_VND', 
                                    title='Salary distribution by category',
                                    labels={'category': 'Category of job position', 'standardize_salary_VND': 'Salary in VND'},
                                    color='category')
    fig_salary_distribution.update_layout(height=600, width=1200)

    # Experience requirement
    experience_counts = df['experience'].value_counts().reset_index()
    experience_counts.columns = ['experience', 'count']
    fig_experience_counts = px.bar(experience_counts, x='count', y='experience', 
                                title='Experience Requirement',
                                labels={'experience': 'Experience', 'count': 'Number of job post'},
                                color='experience')
    fig_experience_counts.update_layout(height=600, width=1200)

    # Location distribution
    location_counts = df['job_location'].value_counts().reset_index()
    location_counts.columns = ['location', 'count']
    fig_location_counts = px.bar(location_counts, x='location', y='count', 
                                title='Job distribution by location',
                                labels={'location': 'Location', 'count': 'Number of job post'},
                                color='location')
    fig_location_counts.update_layout(xaxis_tickangle=-45,height=600, width=1200)

    # Required skills
    skills = df['requirement'].dropna().str.split(',').explode().str.strip()
    skill_counts = skills.value_counts().reset_index()
    skill_counts.columns = ['skill', 'count']
    fig_skill_counts = px.bar(skill_counts.head(20), x='skill', y='count', 
                            title='Top 20 most required skills',
                            labels={'skill': 'Skill', 'count': 'Count'},
                            color='skill')
    fig_skill_counts.update_layout(xaxis_tickangle=-45,height=600, width=1200)

    try:
        os.mkdir('charts/univariate')
    except:
        pass

    timestamp = datetime.now().strftime("%y%m%d%H%m")
    # Show all charts
    fig_job_counts.show()
    fig_salary_distribution.show()
    fig_experience_counts.show()
    fig_location_counts.show()
    fig_skill_counts.show()

    list_fig = [fig_job_counts,fig_salary_distribution, fig_experience_counts, fig_location_counts, fig_skill_counts]
    list_fig_name = ['job_counts', 'salary_distribution', 'experience_counts', 'location_counts', 'skill_counts']
    
    for fig, name in zip(list_fig, list_fig_name):
        try:
            pio.write_image(fig, f"charts/univariate/{name}_{timestamp}.svg")
        except:
            print(f'Chart {name} could not be saved.')
            continue
    
    return list_fig



def create_comparative_charts(df, group_by_columns=['experience', 'job_location'], max_skills=20):
    """
    Creates a set of grouped charts for salary, experience, and skills.

    Args:
    df (DataFrame): The job data.
    group_by_columns (list): List of columns to group by for comparison.
    max_skills (int): Number of top skills to display.

    Returns:
    None
    """
    # Initialize subplots layout
    n_cols = len(group_by_columns)
    fig = make_subplots(
        rows=3, cols=n_cols, 
        subplot_titles=[
            f"{chart} grouped by {group}" 
            for chart in ["Job Count", "Salary Distribution", "Experience Distribution"]
            for group in group_by_columns
        ],
        horizontal_spacing=0.1,
        vertical_spacing=0.15,
    )

    # Iterate over group_by_columns
    for idx, group_by in enumerate(group_by_columns):
        col_idx = idx + 1

        # Job count by group
        job_counts = df[group_by].value_counts().reset_index()
        job_counts.columns = [group_by, 'count']
        fig_job_counts = px.bar(job_counts, x=group_by, y='count', 
                                color=group_by, 
                                labels={group_by: group_by.title(), 'count': 'Job Count'})
        for trace in fig_job_counts.data:
            fig.add_trace(trace, row=1, col=col_idx)

        # Salary distribution
        fig_salary = px.box(df, x=group_by, y='standardize_salary_VND', 
                            color=group_by, 
                            labels={group_by: group_by.title(), 'standardize_salary_VND': 'Salary in VND'})
        for trace in fig_salary.data:
            fig.add_trace(trace, row=2, col=col_idx)

        # Experience distribution
        experience_counts = df['experience'].value_counts().reset_index()
        experience_counts.columns = ['experience', 'count']
        fig_experience = px.bar(experience_counts, y='count', x='experience', 
                                color='experience',
                                labels={'experience': 'Experience Level', 'count': 'Count'})
        for trace in fig_experience.data:
            fig.add_trace(trace, row=3, col=col_idx)



    # Update layout
    fig.update_layout(
        height=1200, width=600 * n_cols,
        title_text="Job Analysis by Various Groups",
        showlegend=False,
    )

    fig.show()

    timestamp = datetime.now().strftime("%y%m%d%H%m")
    try:
        os.mkdir('charts/multivariate/comparation')
    except:
        pass
    try:
        pio.write_image(fig, f"charts/multivariate/comparation_{timestamp}.png")
    except:
        print('Chart could not be saved.')
        


def create_grouped_charts(df, group_by, analysis_columns, max_skills=20):
    """
    Creates grouped charts for each unique value of a column (e.g., location or experience).

    Args:
    df (DataFrame): The job data.
    group_by (str): The column to group by (e.g., "location", "experience").
    analysis_columns (list): Columns to analyze within each group (e.g., "salary", "skill").
    max_skills (int): Maximum number of top skills to display.

    Returns:
    None
    """
    unique_groups = df[group_by].dropna().unique()
    n_rows = len(unique_groups)
    n_cols = len(analysis_columns)

    # Initialize subplots layout
    fig = make_subplots(
        rows=n_rows, cols=n_cols,
        subplot_titles=[
            f"{col} for {group_by}: {group}" 
            for group in unique_groups for col in analysis_columns
        ],
        horizontal_spacing=0.1, vertical_spacing=0.15
    )

    # Iterate over each unique group
    for row_idx, group in enumerate(unique_groups):
        filtered_df = df[df[group_by] == group]
        col_idx = 1  # Reset column index for each group

        for analysis_col in analysis_columns:
            if analysis_col == "standardize_salary_VND":
                # Salary distribution
                salary_fig = px.box(filtered_df, y=analysis_col, 
                                    title=f"Salary for {group}",
                                    labels={analysis_col: "Salary in VND"})
                for trace in salary_fig.data:
                    fig.add_trace(trace, row=row_idx + 1, col=col_idx)

            elif analysis_col == "requirement":
                # Skill distribution
                skills = filtered_df[analysis_col].dropna().str.split(',').explode().str.strip()
                skill_counts = skills.value_counts().head(max_skills).reset_index()
                skill_counts.columns = ['skill', 'count']
                skill_fig = px.bar(skill_counts, x='skill', y='count', 
                                   title=f"Skills for {group}",
                                   labels={'skill': 'Skill', 'count': 'Count'})
                for trace in skill_fig.data:
                    fig.add_trace(trace, row=row_idx + 1, col=col_idx)

            elif analysis_col == "experience":
                # Experience distribution
                exp_counts = filtered_df[analysis_col].value_counts().reset_index()
                exp_counts.columns = ['experience', 'count']
                exp_fig = px.bar(exp_counts, x='experience', y='count', 
                                 title=f"Experience for {group}",
                                 labels={'experience': 'Experience', 'count': 'Count'})
                for trace in exp_fig.data:
                    fig.add_trace(trace, row=row_idx + 1, col=col_idx)

            # Update to the next column
            col_idx += 1

    # Update layout
    fig.update_layout(
        height=300 * n_rows, width=300 * n_cols,
        title_text=f"Analysis by {group_by}",
        showlegend=False
    )
    fig.show()

    timestamp = datetime.now().strftime("%y%m%d%H%m")
    try:
        os.mkdir('charts/multivariate/grouped')
    except:
        pass
    try:
        pio.write_image(fig, f"charts/multivariate/grouped_{timestamp}.png")
    except:
        print('Chart could not be saved.')


def create_grouped_charts_in_batches(df, group_by, analysis_columns, max_skills=20, max_rows=5):
    """
    Creates grouped charts for each unique value of a column in batches to avoid vertical spacing issues.

    Args:
    df (DataFrame): The job data.
    group_by (str): The column to group by (e.g., "location", "experience").
    analysis_columns (list): Columns to analyze within each group (e.g., "salary", "skill").
    max_skills (int): Maximum number of top skills to display.
    max_rows (int): Maximum rows (unique group values) per batch.

    Returns:
    None
    """

    unique_groups = df[group_by].dropna().unique()
    total_groups = len(unique_groups)
    num_batches = math.ceil(total_groups / max_rows)

    for batch_idx in range(num_batches):
        start_idx = batch_idx * max_rows
        end_idx = min(start_idx + max_rows, total_groups)
        groups_in_batch = unique_groups[start_idx:end_idx]
        n_rows = len(groups_in_batch)
        n_cols = len(analysis_columns)

        # Initialize subplots layout for the current batch
        fig = make_subplots(
            rows=n_rows, cols=n_cols,
            subplot_titles=[
                f"{col} for {group_by}: {group}" 
                for group in groups_in_batch for col in analysis_columns
            ],
            horizontal_spacing=0.1, vertical_spacing=0.15
        )

        # Iterate over each group in the batch
        for row_idx, group in enumerate(groups_in_batch):
            filtered_df = df[df[group_by] == group]
            col_idx = 1  # Reset column index for each group

            for analysis_col in analysis_columns:
                if analysis_col == "standardize_salary_VND":
                    # Salary distribution
                    salary_fig = px.box(filtered_df, y=analysis_col, 
                                        title=f"Salary for {group}",
                                        labels={analysis_col: "Salary in VND"})
                    for trace in salary_fig.data:
                        fig.add_trace(trace, row=row_idx + 1, col=col_idx)

                elif analysis_col == "requirement":
                    # Skill distribution
                    skills = filtered_df[analysis_col].dropna().str.split(',').explode().str.strip()
                    skill_counts = skills.value_counts().head(max_skills).reset_index()
                    skill_counts.columns = ['skill', 'count']
                    skill_fig = px.bar(skill_counts, x='skill', y='count', 
                                       title=f"Skills for {group}",
                                       labels={'skill': 'Skill', 'count': 'Count'})
                    for trace in skill_fig.data:
                        fig.add_trace(trace, row=row_idx + 1, col=col_idx)

                elif analysis_col == "experience":
                    # Experience distribution
                    exp_counts = filtered_df[analysis_col].value_counts().reset_index()
                    exp_counts.columns = ['experience', 'count']
                    exp_fig = px.bar(exp_counts, x='experience', y='count', 
                                     title=f"Experience for {group}",
                                     labels={'experience': 'Experience', 'count': 'Count'})
                    for trace in exp_fig.data:
                        fig.add_trace(trace, row=row_idx + 1, col=col_idx)

                elif analysis_col == "job_location":
                    # Location distribution
                    location_counts = filtered_df[analysis_col].value_counts().reset_index()
                    location_counts.columns = ['job_location', 'count']
                    location_fig = px.bar(location_counts, x='job_location', y='count', 
                                     title=f"Location for {group}",
                                     labels={'job_location': 'Location', 'count': 'Count'})
                    for trace in location_fig.data:
                        fig.add_trace(trace, row=row_idx + 1, col=col_idx)

                # Update to the next column
                col_idx += 1



        # Update layout and show the batch figure
        fig.update_layout(
            height=450 * n_rows, width=510 * n_cols,
            title_text=f"Analysis by {group_by} (Batch {batch_idx + 1})",
            showlegend=False
        )
        fig.show()


        timestamp = datetime.now().strftime("%y%m%d%H%m")
        try:
            os.mkdir('charts/multivariate/groupedbatch')
        except:
            pass
        try:
            pio.write_image(fig, f"charts/multivariate/groupedbatch_{timestamp}.png")
        except:
            print('Chart could not be saved.')

        # # Save the figure to an HTML file
        # output_file = os.path.join('charts', f"{datetime.now().strftime('%y%m%d-%H%M')}_{group_by}_batch_{batch_idx + 1}.html")
        # fig.write_html(output_file)
        # print(f"Saved batch {batch_idx + 1} to {output_file}")

def create_scatter_3d(df, x_col, y_col, z_col, color_col):
    """
    Create a 3D scatter plot to show the correlation between three numerical variables.

    Args:
    df (DataFrame): The input data.
    x_col (str): Column name for the x-axis.
    y_col (str): Column name for the y-axis.
    z_col (str): Column name for the z-axis.
    color_col (str): Column name for the color dimension (categorical or numerical).

    Returns:
    fig (Figure): A Plotly 3D scatter plot figure.
    """
    # Create a 3D scatter plot
    fig = px.scatter_3d(
        df,
        x=x_col,
        y=y_col,
        z=z_col,
        color=color_col,
        title=f"3D Scatter Plot of {x_col}, {y_col}, {z_col} grouped by {color_col}",
        labels={
            x_col: x_col.replace('_', ' ').title(),
            y_col: y_col.replace('_', ' ').title(),
            z_col: z_col.replace('_', ' ').title(),
            color_col: color_col.replace('_', ' ').title()
        },
        opacity=0.7
    )

    # Update layout
    fig.update_layout(
        height=800,
        scene=dict(
            xaxis_title=x_col.replace('_', ' ').title(),
            yaxis_title=y_col.replace('_', ' ').title(),
            zaxis_title=z_col.replace('_', ' ').title(),
        ),
        margin=dict(l=0, r=0, b=0, t=40),
        legend=dict(title=color_col.replace('_', ' ').title()),
    )

    timestamp = datetime.now().strftime("%y%m%d%H%m")
    try:
        os.mkdir('charts/multivariate/scatter')
    except:
        pass
    try:
        pio.write_image(fig, f"charts/multivariate/scatter_{timestamp}.png")
    except:
        print('Chart could not be saved.')

    return fig
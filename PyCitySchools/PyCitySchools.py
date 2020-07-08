#!/usr/bin/env python
# coding: utf-8

# ### Note
# * Instructions have been included for each segment. You do not have to follow them exactly, but they are included to help you think through the steps.

# In[668]:


# Dependencies and Setup
import pandas as pd

# File to Load (Remember to Change These)
school_data_to_load = "Resources/schools_complete.csv"
student_data_to_load = "Resources/students_complete.csv"

# Read School and Student Data File and store into Pandas DataFrames
school_data = pd.read_csv(school_data_to_load)
student_data = pd.read_csv(student_data_to_load)

# Combine the data into a single dataset.  
school_data_complete = pd.merge(student_data, school_data, how="left", on=["school_name", "school_name"])
school_data_complete.head()


# ## District Summary
# 
# * Calculate the total number of schools
# 
# * Calculate the total number of students
# 
# * Calculate the total budget
# 
# * Calculate the average math score 
# 
# * Calculate the average reading score
# 
# * Calculate the percentage of students with a passing math score (70 or greater)
# 
# * Calculate the percentage of students with a passing reading score (70 or greater)
# 
# * Calculate the percentage of students who passed math **and** reading (% Overall Passing)
# 
# * Create a dataframe to hold the above results
# 
# * Optional: give the displayed data cleaner formatting

# In[684]:


district_totals = school_data_complete.nunique()
district_totals.head(11)


# In[685]:


# Check for any null values
# school_data_complete.isnull().sum().sum()


# In[686]:


# Calculate the total number of schools
total_schools = district_totals["School ID"]
#total_schools

# Calculate the total number of students
total_students = district_totals["Student ID"]
#total_students

# Calculate the total budget
total_budget = school_data["budget"].sum()
#total_budget

# Calculate the average math score
avg_math = student_data["math_score"].mean()
#avg_math

# Calculate the average reading score
avg_read = student_data["reading_score"].mean()
#avg_read


# Calculate the percentage of students with a passing math score (70 or greater)
math_pass = len(school_data_complete.loc[school_data_complete["math_score"]>=70])
math_pass_percent = (math_pass/total_students) *100
#math_pass_percent

# Calculate the percentage of students with a passing reading score (70 or greater)
read_pass = len(school_data_complete.loc[school_data_complete["reading_score"]>=70])
read_pass_percent = (read_pass/total_students) *100
#read_pass_percent

# Calculate the percentage of students who passed math and reading (% Overall Passing)
both_pass = len(school_data_complete.loc[(school_data_complete["math_score"]>=70) & (school_data_complete["reading_score"]>=70)])
both_percent = (both_pass/total_students) *100
#both_percent


# In[687]:


#Create a dataframe to hold the above results
district_summary =pd.DataFrame({"Total Schools": [total_schools], 
                                "Total Student": [total_students],
                                "Total Budget": [total_budget], 
                                "Average Math Score": [avg_math],
                                "Average Reading Score": [avg_read],
                                "% Passing Math": [math_pass_percent],
                                "% Passing Reading": [read_pass_percent],
                                "% Overall Passing": [both_percent]}) 

# Optional: give the displayed data cleaner formatting
district_summary["Total Student"] = district_summary["Total Student"].map("{:,}".format)
district_summary["Total Budget"] = district_summary["Total Budget"].map("${:,.2f}".format)
district_summary


# # School Summary

# * Create an overview table that summarizes key metrics about each school, including:
#   * School Name
#   * School Type
#   * Total Students
#   * Total School Budget
#   * Per Student Budget
#   * Average Math Score
#   * Average Reading Score
#   * % Passing Math
#   * % Passing Reading
#   * % Overall Passing (The percentage of students that passed math **and** reading.)
#   
# * Create a dataframe to hold the above results

# In[688]:


# School Name and Type
school_type = school_data.set_index(["school_name"])["type"]

# Group by and merge data
school_total = school_data_complete.groupby(["school_name"]).mean()
school_total = pd.merge(school_type, school_total, on="school_name")


# Total Students per school
total_stu_per_school = school_total["size"]


# Total School Budget per school
school_budget = school_total["budget"]


# Per Student Budget per school
student_budget = school_total["budget"]/school_total["size"]


# Average Math Score per school
math_school_avg = school_total["math_score"]


# Average Reading Score per school
read_school_avg = school_total["reading_score"]


# % Passing Math
math_schools = school_data_complete.loc[school_data_complete["math_score"]>=70, ["school_name","math_score"]]
math_schools = math_schools.groupby(["school_name"]).count()


# % Passing Reading
read_schools = school_data_complete.loc[school_data_complete["reading_score"]>=70, ["school_name","reading_score"]]
read_schools = read_schools.groupby(["school_name"]).count()


# % Overall Passing (The percentage of students that passed math and reading.)
overall_schools = school_data_complete.loc[(school_data_complete["math_score"]>=70) & (school_data_complete["reading_score"]>=70), ["school_name", "reading_score"]]
overall_schools = overall_schools.groupby(["school_name"]).count()


# Add new columns to DataFrame
school_total["Per Student Budget"] = school_total["budget"]/school_total["size"]
school_total["% Passing Math"] = (math_schools["math_score"]/total_stu_per_school)*100
school_total["% Passing Reading"] = (read_schools["reading_score"]/total_stu_per_school)*100
school_total["% Overall Passing"] = (overall_schools["reading_score"]/total_stu_per_school)*100

# Remove unwanted columns
school_total.pop("Student ID")
school_total.pop("School ID")

# Sort school names alphabetically
school_results = school_total.sort_values(["school_name"], ascending=True)


# In[689]:


# Create a dataframe to hold the above results

# Reorganize the columns
school_summary = school_results[["type",
                                 "size",
                                 "budget",
                                 "Per Student Budget",
                                 "math_score",
                                 "reading_score",
                                 "% Passing Math",
                                 "% Passing Reading",
                                 "% Overall Passing"]]



# Rename the columns
school_summary = school_summary.rename(columns={"type":"School Type",
                                                "size":"Total Students",
                                                "budget":"Total School Budget",
                                                "math_score":"Average Math Score",
                                                "reading_score":"Average Reading Score"})



# Remove the index header
school_summary.index.name = None


# Give the displayed data cleaner formatting
school_summary["Total Students"] = school_summary["Total Students"].map("{:.0f}".format)
school_summary["Total School Budget"] = school_summary["Total School Budget"].map("${:,.2f}".format)
school_summary["Per Student Budget"] = school_summary["Per Student Budget"].map("${:.2f}".format)

# Display DataFrame
school_summary


# In[ ]:





# ## Top Performing Schools (By % Overall Passing)

# * Sort and display the top five performing schools by % overall passing.

# In[676]:


# Sort and display top five performing schools by % overall passing

top_five = school_summary.sort_values(["% Overall Passing"], ascending=False)
top_five.head(5)


# In[ ]:





# ## Bottom Performing Schools (By % Overall Passing)

# * Sort and display the five worst-performing schools by % overall passing.

# In[677]:


# Sort and display the five worst-performing schools by % overall passing

bottom_five = school_summary.sort_values(["% Overall Passing"], ascending=True)
bottom_five.head(5)


# ## Math Scores by Grade

# * Create a table that lists the average Math Score for students of each grade level (9th, 10th, 11th, 12th) at each school.
# 
#   * Create a pandas series for each grade. Hint: use a conditional statement.
#   
#   * Group each series by school
#   
#   * Combine the series into a dataframe
#   
#   * Optional: give the displayed data cleaner formatting

# In[690]:


# Create a series for each grade
grades = school_data_complete.set_index(["school_name"])["grade"]
grades

math_ninth = school_data_complete.loc[school_data_complete["grade"]=="9th", ["school_name","math_score"]]
math_ninth_avg = math_ninth.groupby(["school_name"]).mean()
math_ninth_avg

math_tenth = school_data_complete.loc[school_data_complete["grade"]=="10th", ["school_name","math_score"]]
math_tenth_avg = math_tenth.groupby(["school_name"]).mean()
math_tenth_avg

math_eleventh = school_data_complete.loc[school_data_complete["grade"]=="11th", ["school_name","math_score"]]
math_eleventh_avg = math_eleventh.groupby(["school_name"]).mean()
math_eleventh_avg

math_twelfth = school_data_complete.loc[school_data_complete["grade"]=="12th", ["school_name","math_score"]]
math_twelfth_avg = math_twelfth.groupby(["school_name"]).mean()
math_twelfth_avg


# Add new columns to DataFrame
math_ninth_avg["10th"] = math_tenth_avg
math_ninth_avg["11th"] = math_eleventh_avg
math_ninth_avg["12th"] = math_twelfth_avg
math_ninth_avg

# Rename the DataFrame and columns
math_by_grade = math_ninth_avg.rename(columns={"math_score":"9th"})
math_by_grade

# Remove the index header
math_by_grade.index.name = None
math_by_grade


# In[ ]:





# ## Reading Score by Grade 

# * Perform the same operations as above for reading scores

# In[691]:


# Create a series for each grade
grades = school_data_complete.set_index(["school_name"])["grade"]
grades

read_ninth = school_data_complete.loc[school_data_complete["grade"]=="9th", ["school_name","reading_score"]]
read_ninth_avg = read_ninth.groupby(["school_name"]).mean()
read_ninth_avg

read_tenth = school_data_complete.loc[school_data_complete["grade"]=="10th", ["school_name","reading_score"]]
read_tenth_avg = read_tenth.groupby(["school_name"]).mean()
read_tenth_avg

read_eleventh = school_data_complete.loc[school_data_complete["grade"]=="11th", ["school_name","reading_score"]]
read_eleventh_avg = read_eleventh.groupby(["school_name"]).mean()
read_eleventh_avg

read_twelfth = school_data_complete.loc[school_data_complete["grade"]=="12th", ["school_name","reading_score"]]
read_twelfth_avg = read_twelfth.groupby(["school_name"]).mean()
read_twelfth_avg


# Add new columns to DataFrame
read_ninth_avg["10th"] = read_tenth_avg
read_ninth_avg["11th"] = read_eleventh_avg
read_ninth_avg["12th"] = read_twelfth_avg
read_ninth_avg

# Rename the DataFrame and columns
read_by_grade = read_ninth_avg.rename(columns={"reading_score":"9th"})
read_by_grade

# Remove the index header
read_by_grade.index.name = None
read_by_grade


# In[ ]:





# ## Scores by School Spending

# * Create a table that breaks down school performances based on average Spending Ranges (Per Student). Use 4 reasonable bins to group school spending. Include in the table each of the following:
#   * Average Math Score
#   * Average Reading Score
#   * % Passing Math
#   * % Passing Reading
#   * Overall Passing Rate (Average of the above two)

# In[692]:


# Create the bins in which data will be held
bins = [0, 584.9, 629.9, 644.9, 675]


# Create the names for the four bins
group_names = ["<$584", "$585-629", "$630-644", "$645-675"]


# Cut the bins
school_total["Spending Ranges (Per Student)"] = pd.cut(school_total["Per Student Budget"], bins, labels=group_names, include_lowest=True)


# Groupby spending ranges
school_spending_group = school_total.groupby(["Spending Ranges (Per Student)"]).mean()
school_spending_group


# Reorganize the columns
school_spending = school_spending_group[["math_score",
                                 "reading_score",
                                 "% Passing Math",
                                 "% Passing Reading",
                                 "% Overall Passing"]]


# Rename the columns
school_spending = school_spending.rename(columns={"math_score":"Average Math Score",
                                                "reading_score":"Average Reading Score"})

# Give the displayed data cleaner formatting
school_spending["Average Math Score"] = school_spending["Average Math Score"].map("{:.2f}".format)
school_spending["Average Reading Score"] = school_spending["Average Reading Score"].map("{:.2f}".format)
school_spending["% Passing Math"] = school_spending["% Passing Math"].map("{:.2f}".format)
school_spending["% Passing Reading"] = school_spending["% Passing Reading"].map("{:.2f}".format)
school_spending["% Overall Passing"] = school_spending["% Overall Passing"].map("{:.2f}".format)

school_spending


# In[ ]:





# ## Scores by School Size

# * Perform the same operations as above, based on school size.

# In[693]:


# Create the bins in which data will be held
bins = [0, 999.9, 1999.9, 4999.9]


# Create the names for the three bins
group_names = ["Small(<1000)", "Medium (1000-2000)", "Large(2000-5000)"]


# Cut the bins
school_total["School Size"] = pd.cut(school_total["size"], bins, labels=group_names, include_lowest=True)


# Groupby size ranges
school_size_group = school_total.groupby(["School Size"]).mean()
school_size_group


# Reorganize the columns
school_size = school_size_group[["math_score",
                                 "reading_score",
                                 "% Passing Math",
                                 "% Passing Reading",
                                 "% Overall Passing"]]


# Rename the columns
school_size = school_size.rename(columns={"math_score":"Average Math Score",
                                          "reading_score":"Average Reading Score"})

# Give the displayed data cleaner formatting
school_size["Average Math Score"] = school_size["Average Math Score"].map("{:.2f}".format)
school_size["Average Reading Score"] = school_size["Average Reading Score"].map("{:.2f}".format)
school_size["% Passing Math"] = school_size["% Passing Math"].map("{:.2f}".format)
school_size["% Passing Reading"] = school_size["% Passing Reading"].map("{:.2f}".format)
school_size["% Overall Passing"] = school_size["% Overall Passing"].map("{:.2f}".format)

school_size


# ## Scores by School Type

# * Perform the same operations as above, based on school type

# In[694]:


school_total = school_total.rename(columns={"type": "School Type"})

# Groupby school type
school_type_group = school_total.groupby(["School Type"]).mean()
school_type_group

# Reorganize the columns
school_type = school_type_group[["math_score",
                                 "reading_score",
                                 "% Passing Math",
                                 "% Passing Reading",
                                 "% Overall Passing"]]

# Rename the columns
school_type = school_type.rename(columns={"math_score":"Average Math Score",
                                          "reading_score":"Average Reading Score"})


school_type


# In[ ]:





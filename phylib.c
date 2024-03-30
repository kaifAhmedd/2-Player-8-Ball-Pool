#include "phylib.h"
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

// function makes a new still ball. 
// we malloc for a new object
// if object is null then we return null otherwise we set objects number,pos, and type and return object
phylib_object *phylib_new_still_ball(unsigned char number, phylib_coord *pos){
    phylib_object * object = malloc(sizeof(phylib_object));
    
    if(object == NULL){
        return NULL;
    }
    object->obj.still_ball.number = number;
    object->obj.still_ball.pos = *pos;
    object->type = PHYLIB_STILL_BALL;
    return object;
}

// function makes a new rolling ball. we allocate memory for it. if null then we return null. we set the number, pos, vel, acc, type and return
phylib_object *phylib_new_rolling_ball(unsigned char number, phylib_coord *pos, phylib_coord *vel, phylib_coord *acc){
    phylib_object * object = malloc(sizeof(phylib_object));

    if(object == NULL){
        return NULL;
    }
    object->obj.rolling_ball.number = number;
    object->obj.rolling_ball.pos = *pos;
    object->obj.rolling_ball.vel = *vel;
    object->obj.rolling_ball.acc = *acc;
    object->type = PHYLIB_ROLLING_BALL;
    return object;
}

// we malloc for new hole. if null we return null. we then set its pos and type and return the hole
phylib_object *phylib_new_hole(phylib_coord *pos){
    phylib_object * object = malloc(sizeof(phylib_object));

    if(object == NULL){
        return NULL;
    }
    object->obj.hole.pos = *pos;
    object->type = PHYLIB_HOLE;
    return object;
}

// we malloc for new hcushion if null we return null otherwise we sent the y pos and type before returning
phylib_object *phylib_new_hcushion(double y){
    phylib_object * object = malloc(sizeof(phylib_object));

    if(object == NULL){
        return NULL;
    }

    object->obj.hcushion.y = y;
    object->type = PHYLIB_HCUSHION;
    return object;
}

// we allocate for vcushion if null we return null, otherwise we set x position and type before returning
phylib_object *phylib_new_vcushion(double x){
    phylib_object * object = malloc(sizeof(phylib_object));

    if(object == NULL){
        return NULL;
    }

    object->obj.vcushion.x = x;
    object->type = PHYLIB_VCUSHION;
    return object;
}

// we allocate for new table. if null we return null otherwise we set each object to what the table has and et the rest of the elements to null
// before returning the table. we set the tables time to 0.0
phylib_table *phylib_new_table(void){
    phylib_table * table = malloc(sizeof(phylib_table));

    if(table == NULL){
        return NULL;
    }

    table->time = 0.0;
    table->object[0] = phylib_new_hcushion(0.0);
    table->object[1] = phylib_new_hcushion(PHYLIB_TABLE_LENGTH);
    table->object[2] = phylib_new_vcushion(0.0);
    table->object[3] = phylib_new_vcushion(PHYLIB_TABLE_WIDTH);
    table->object[4] = phylib_new_hole(&(phylib_coord){0.0, 0.0});
    table->object[5] = phylib_new_hole(&(phylib_coord){0.0, (PHYLIB_TABLE_LENGTH/2)});
    table->object[6] = phylib_new_hole(&(phylib_coord){0.0, PHYLIB_TABLE_LENGTH});
    table->object[7] = phylib_new_hole(&(phylib_coord){PHYLIB_TABLE_WIDTH, 0.0});
    table->object[8] = phylib_new_hole(&(phylib_coord){PHYLIB_TABLE_WIDTH, (PHYLIB_TABLE_LENGTH/2)});
    table->object[9] = phylib_new_hole(&(phylib_coord){PHYLIB_TABLE_WIDTH, PHYLIB_TABLE_LENGTH});

    for(int i = 10; i<PHYLIB_MAX_OBJECTS; i++){
        table->object[i] = NULL;
    }
    return table;
}

// function allocates space for dest. if soruce is null then we set dest to null. if dest is not null then we copy
// contents of source to dest othersiw we set dest to null
void phylib_copy_object(phylib_object **dest, phylib_object **src){
    *dest = malloc(sizeof(phylib_object));
    if(*src == NULL){
        *dest = NULL;
    }
    if(*dest != NULL){
        memcpy(*dest, *src, sizeof(phylib_object));
    }
    else{
        *dest = NULL;
    }
}

// if table null we return null. otherwise we allocate for newtable and if it null we return null otherwise we
//set old tables contents to new tables contents before returning the new table
phylib_table *phylib_copy_table(phylib_table *table){
    if(table == NULL){
        return NULL;
    }
    phylib_table * newTable = calloc(1,sizeof(phylib_table));

    if(newTable == NULL){
        return NULL;
    }
    newTable->time = table->time;
    for(int i = 0; i<PHYLIB_MAX_OBJECTS; i++){
        if(table->object[i] != NULL){
            phylib_copy_object(&newTable->object[i], &table->object[i]);
        }
    }
    return newTable;
}

// we go over each object if object at index i is null then we set that obect to object before leaving the function
void phylib_add_object(phylib_table *table, phylib_object *object){
    for(int i=0; i<PHYLIB_MAX_OBJECTS; i++){
        if(table->object[i] == NULL){
            table->object[i] = object;
            break;
        }
    }
}


// function goes over each object in table and if object is not null we free the object before freeing the whole table
void phylib_free_table(phylib_table *table){
    for(int i = 0; i<PHYLIB_MAX_OBJECTS; i++){
        if(table->object[i] != NULL){
            free(table->object[i]);
        }
    }
    free(table);
}

//This function returns the difference between c1 and c2. we calculate for x difference and y difference 
phylib_coord phylib_sub(phylib_coord c1, phylib_coord c2){
    double xDifference = c1.x - c2.x;
    double yDifference = c1.y - c2.y;
   return (phylib_coord){xDifference, yDifference};
}

// we calculate length by doing x*x and y*y of coord c and take sqare root of their sum and return
double phylib_length(phylib_coord c){
    double expX = c.x * c.x;
    double expY = c.y * c.y;
    double sum = expX + expY;
    return sqrt(sum);
}

// we do the dot product of two coords by mutiplying x and y componets and adding them together before returning
double phylib_dot_product(phylib_coord a, phylib_coord b){
    return (a.x * b.x) + (a.y * b.y);
}

// if obj 1 is not rollig ball then we return -1.0
//If obj2 is another BALL ( ROLLING or STILL), then we get distance of two balls and sutract ball diameter
//If obj2 is a HOLE, then we get distance of ball and hole and subtract hole radius
//If obj2 is a CUSHION then we get distance betweem the ball and cushion and subtract ball radius.
// we Return -1.0 if obj2 isn’t any fo the types
double phylib_distance(phylib_object *obj1, phylib_object *obj2){
    if(obj1->type != PHYLIB_ROLLING_BALL){
        return -1.0;
    }
    phylib_coord position = obj1->obj.rolling_ball.pos;
    if(obj2->type == PHYLIB_ROLLING_BALL){
        phylib_coord distance_rolling = phylib_sub(position, obj2->obj.rolling_ball.pos);
        return phylib_length(distance_rolling) - PHYLIB_BALL_DIAMETER;
    }
    if(obj2->type == PHYLIB_STILL_BALL){
        phylib_coord distance_still = phylib_sub(position, obj2->obj.still_ball.pos);
        return phylib_length(distance_still) - PHYLIB_BALL_DIAMETER;
    }
    if(obj2->type == PHYLIB_HOLE){
        phylib_coord distance_hole = phylib_sub(position, obj2->obj.hole.pos);
        return phylib_length(distance_hole) - PHYLIB_HOLE_RADIUS;
    }
    if(obj2->type == PHYLIB_VCUSHION){
        return fabs(position.x - obj2->obj.vcushion.x) - PHYLIB_BALL_RADIUS;
    }
    if(obj2->type == PHYLIB_HCUSHION){
        return fabs(position.y - obj2->obj.hcushion.y) - PHYLIB_BALL_RADIUS;
    }
    return -1.0;
}

// if new and old objects arent rolling balls then we end the program
// otherwise we do many caculations listed in the assingment docs for the new ojects posision and velocity
// we check if signs of velocitions changed of old and new object and if so then we set new objects
// velocity and acceleratiosn to 0
void phylib_roll(phylib_object *new, phylib_object *old, double time){
    if(new->type != PHYLIB_ROLLING_BALL && old->type != PHYLIB_ROLLING_BALL){
        return;
    }
    else{
        double time_exp = time * time;
        new->obj.rolling_ball.pos.x = (old->obj.rolling_ball.pos.x) + 
        (old->obj.rolling_ball.vel.x * time) + (0.5 * old->obj.rolling_ball.acc.x * time_exp);

        new->obj.rolling_ball.pos.y = (old->obj.rolling_ball.pos.y) + 
        (old->obj.rolling_ball.vel.y * time) + (0.5 * old->obj.rolling_ball.acc.y * time_exp);

        new->obj.rolling_ball.vel.x = (old->obj.rolling_ball.vel.x) + (old->obj.rolling_ball.acc.x * time);
        new->obj.rolling_ball.vel.y = (old->obj.rolling_ball.vel.y) + (old->obj.rolling_ball.acc.y * time);

        if(new->obj.rolling_ball.vel.x >=0.0 && old->obj.rolling_ball.vel.x <=0.0){
            new->obj.rolling_ball.vel.x = 0.0;
            new->obj.rolling_ball.acc.x = 0.0;

        }
        if(new->obj.rolling_ball.vel.x <=0.0 && old->obj.rolling_ball.vel.x >=0.0){
            new->obj.rolling_ball.vel.x = 0.0;
            new->obj.rolling_ball.acc.x = 0.0;

        }

        if(new->obj.rolling_ball.vel.y >=0.0 && old->obj.rolling_ball.vel.y <=0.0){
            new->obj.rolling_ball.vel.y = 0.0;
            new->obj.rolling_ball.acc.y = 0.0;

        }
        if(new->obj.rolling_ball.vel.y <=0.0 && old->obj.rolling_ball.vel.y >=0.0){
            new->obj.rolling_ball.vel.y = 0.0;
            new->obj.rolling_ball.acc.y = 0.0;
        }
    }
}


// if our object is a rolling ball and if velocity is less than epsilon then we turn rolling ball to a still ball
// using the function we created and return 1 otherwise we return 0.
unsigned char phylib_stopped(phylib_object *object){
    if(object->type == PHYLIB_ROLLING_BALL && fabs(object->obj.rolling_ball.vel.x) < PHYLIB_VEL_EPSILON && fabs(object->obj.rolling_ball.vel.y) < PHYLIB_VEL_EPSILON){
        phylib_coord conversion = object->obj.rolling_ball.pos;
        *object = *phylib_new_still_ball(object->obj.rolling_ball.number, &conversion);
        return 1;
    }
    else{
        return 0;
    }
}

//if object b is a hcushion or vcushion then we set object a vel and acceleration to their negated values
// if object b is a hole then we free object a and set it to null
// if object b is a still ball then we convet it to a rolling ball which automatically takes us to our next case
// if object b is a rolling ball then we do many calculations which are stored in various variables for one final 
// calculation.
// we use many functions we previously created for these calculations as well
// if speed a and speeb b are greater than epsilon then we set acceleration to negated velocity divided by speed
// multipled by phylib drag constant
void phylib_bounce(phylib_object **a, phylib_object **b){
    if((*b)->type == PHYLIB_HCUSHION){
        (*a)->obj.rolling_ball.vel.y = -(*a)->obj.rolling_ball.vel.y;
        (*a)->obj.rolling_ball.acc.y = -(*a)->obj.rolling_ball.acc.y;
    }
    if((*b)->type == PHYLIB_VCUSHION){
        (*a)->obj.rolling_ball.vel.x = -(*a)->obj.rolling_ball.vel.x;
        (*a)->obj.rolling_ball.acc.x = -(*a)->obj.rolling_ball.acc.x;
    }
    if((*b)->type == PHYLIB_HOLE){
        free(*a);
        *a = NULL;
    }
    if((*b)->type == PHYLIB_STILL_BALL){
        phylib_object * oldB;
        oldB = *b;
        phylib_coord coord = (*b)->obj.still_ball.pos;
        phylib_coord vel;
        vel.x = 0;
        vel.y = 0;
        phylib_coord acc;
        acc.x = 0;
        acc.y = 0;
        (*b) = phylib_new_rolling_ball((*b)->obj.still_ball.number, &coord, &vel, &acc);
        free(oldB);
    }
    if((*b)->type == PHYLIB_ROLLING_BALL){
        phylib_coord r_ab;
        r_ab.x = (*a)->obj.rolling_ball.pos.x - (*b)->obj.rolling_ball.pos.x;
        r_ab.y = (*a)->obj.rolling_ball.pos.y - (*b)->obj.rolling_ball.pos.y;

        phylib_coord v_rel;
        v_rel.x = (*a)->obj.rolling_ball.vel.x - (*b)->obj.rolling_ball.vel.x;
        v_rel.y = (*a)->obj.rolling_ball.vel.y - (*b)->obj.rolling_ball.vel.y;

        phylib_coord n;
        n.x = r_ab.x / phylib_length(r_ab);
        n.y = r_ab.y / phylib_length(r_ab);

        double v_rel_n = 0.0;
        v_rel_n = phylib_dot_product(v_rel, n);

        (*a)->obj.rolling_ball.vel.x = (*a)->obj.rolling_ball.vel.x - (v_rel_n * n.x);
        (*a)->obj.rolling_ball.vel.y = (*a)->obj.rolling_ball.vel.y - (v_rel_n * n.y);

        (*b)->obj.rolling_ball.vel.x = (*b)->obj.rolling_ball.vel.x + (v_rel_n * n.x);
        (*b)->obj.rolling_ball.vel.y = (*b)->obj.rolling_ball.vel.y + (v_rel_n * n.y);

        double speed_a = phylib_length((*a)->obj.rolling_ball.vel);
        double speed_b = phylib_length((*b)->obj.rolling_ball.vel);
        if(speed_a > PHYLIB_VEL_EPSILON){
            (*a)->obj.rolling_ball.acc.x = -(*a)->obj.rolling_ball.vel.x/(speed_a) * PHYLIB_DRAG;
            (*a)->obj.rolling_ball.acc.y = -(*a)->obj.rolling_ball.vel.y/(speed_a) * PHYLIB_DRAG;
        }
        if(speed_b > PHYLIB_VEL_EPSILON){
            (*b)->obj.rolling_ball.acc.x = -(*b)->obj.rolling_ball.vel.x/(speed_b) * PHYLIB_DRAG;
            (*b)->obj.rolling_ball.acc.y = -(*b)->obj.rolling_ball.vel.y/(speed_b) * PHYLIB_DRAG;
        }
    }
}

// we go over each object and if objec tis a  rolling ball we add one to the counter and return it in the end
unsigned char phylib_rolling(phylib_table *t){
    int rolling_Balls = 0;
    for(int i=0; i<PHYLIB_MAX_OBJECTS; i++){
        if(t->object[i] != NULL){
            if(t->object[i]->type == PHYLIB_ROLLING_BALL){
                rolling_Balls++;
            }
        }
    }
    return rolling_Balls;
}

// if there are no rolling balls on the table then we return null
// we define a new table and set time to sim rate
// we make the outmost loop that goes on until time is > than sim rate
// we make a for loop that goes over each object and if object is not null and its a rolling ball 
// then we use phylib roll function and if oject has stopped then we increment table time by time and return table
// we then amke a nested for loop that does null checks for both objects and see that if the distance
//between the two is <0.0 we use phylib bounce function and increment table time by time and return table
// to make while loop stop we increment time variable by sim rate.
phylib_table *phylib_segment(phylib_table *table){
    if(phylib_rolling(table) == 0)
    {
        return NULL;
    }

    phylib_table *newTable = phylib_copy_table(table);
    if(newTable == NULL){
        return NULL;
    }
    double time = PHYLIB_SIM_RATE;

    while(time < PHYLIB_MAX_TIME)
    {
        for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++)
        {
            if (newTable->object[i] != NULL && newTable->object[i]->type == PHYLIB_ROLLING_BALL)
            {
                phylib_roll(newTable->object[i], table->object[i], time);

                if(phylib_stopped(newTable->object[i]) == 1)
                {
                    newTable->time += time;
                    return newTable;
                }
            }
        }

        for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++)
        {
            if(newTable->object[i] != NULL && newTable->object[i]->type == PHYLIB_ROLLING_BALL)
            {
                for(int j = 0; j < PHYLIB_MAX_OBJECTS; j++)
                {
                    if(i != j && newTable->object[j] != NULL && phylib_distance(newTable->object[i], newTable->object[j]) < 0.0)
                    {
                        phylib_bounce(&newTable->object[i], &newTable->object[j]);
                        newTable->time += time;
                        return newTable;

                    }
                }
            }
        }
        time += PHYLIB_SIM_RATE;
    }
    return newTable;
}

// this is the function we copy and paste for part 1 of assignment 2
char *phylib_object_string(phylib_object *object){
    static char string[80];
    if (object==NULL){
        snprintf( string, 80, "NULL;" );
        return string;
    }
    switch (object->type){
        case PHYLIB_STILL_BALL:
            snprintf(string, 80,
                    "STILL_BALL (%d,%6.1lf,%6.1lf)",
                    object->obj.still_ball.number,
                    object->obj.still_ball.pos.x,
                    object->obj.still_ball.pos.y);
        break;
        case PHYLIB_ROLLING_BALL:
            snprintf(string, 80,
                    "ROLLING_BALL (%d,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf)",
                    object->obj.rolling_ball.number,
                    object->obj.rolling_ball.pos.x,
                    object->obj.rolling_ball.pos.y,
                    object->obj.rolling_ball.vel.x,
                    object->obj.rolling_ball.vel.y,
                    object->obj.rolling_ball.acc.x,
                    object->obj.rolling_ball.acc.y);
        break;
        case PHYLIB_HOLE:
            snprintf(string, 80,
                    "HOLE (%6.1lf,%6.1lf)",
                    object->obj.hole.pos.x,
                    object->obj.hole.pos.y);
        break;
        case PHYLIB_HCUSHION:
            snprintf(string, 80,
                    "HCUSHION (%6.1lf)",
                    object->obj.hcushion.y);
        break;
        case PHYLIB_VCUSHION:
            snprintf(string, 80,
                    "VCUSHION (%6.1lf)",
                    object->obj.vcushion.x);
        break;
    }
    return string;
}

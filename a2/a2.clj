(ns mainproject-v1.1
  (:require [clojure.set :as set]))

(defn not-elimination
  [not-prop]
  ;; defining local scope variables
  (let [logical-operator (first not-prop)
        second-prop (second not-prop)]
    ;; checking if the second data type is
    (if (= (type second-prop) clojure.lang.PersistentList)
      (if (and (= logical-operator 'not) (= (first second-prop) 'not))
        #{(second second-prop)}
        )
      nil
      )
    ))


(defn and-elimination [and-prop]
  (if (and (= (first and-prop) 'and) (= (count and-prop) 3))
    (set [(second and-prop) (last and-prop)])
    nil
    )
  )

(defn modus-ponens
  [if-prop kb]
  (if (= (count if-prop) 1)
    ; iterating over the knowledge base if there is only a single prop given
    (let [list-kb (into '() kb)
          symbol-prop (first if-prop)
          ]
      (loop [num 0]
        (let [cur-kb-selected (nth list-kb num)
              output (if (list? cur-kb-selected)
                       (if (= (first cur-kb-selected) 'if)
                         (if (= (second cur-kb-selected) symbol-prop)
                           (into #{} (set [(nth cur-kb-selected 2)])))
                         ))]
        (if (or (= (- (count list-kb) 1) num) (not (empty? output)))
          output
          (recur (inc num))
          )
          )

        ))
    ;; normal modus ponens
    (if (and (= (first if-prop) 'if) (= (count if-prop) 3))
      (if (contains? kb (second if-prop))
        (set [(last if-prop)])
        )
      nil))
    )


(defn modus-tollens
  (if (and (= (first if-prop) 'if) (= (count if-prop) 3))
    (if (contains? kb `(~'not ~(last if-prop)))
      ; format into cons (not a) --> persistant list (not a) --> set #{not a}
      (set [(into '() `(~(second if-prop) ~'not))])
      )
    nil
    )
  )

(defn elim-step
  "One step of the elimination inference procedure."
  [prop kb]
    (cond
      (not-elimination prop) (not-elimination prop)
      (and-elimination prop) (and-elimination prop)
      (modus-ponens prop kb) (modus-ponens prop kb)
      (modus-tollens prop kb) (modus-tollens prop kb)
      :else #{}
      )
  )

(defn fwd-infer
  [prop kb]
  (loop
    [cur-prop prop
     cur-kb kb]
    (let [output-prop (elim-step (if (instance? clojure.lang.Symbol cur-prop) (list cur-prop) cur-prop) cur-kb)]
      (if (empty? output-prop)
        (set/union (if (= (count cur-prop) 1) (hash-set (first cur-prop) ) (hash-set cur-prop) ) cur-kb output-prop)
        (recur
          (if (= (type (first output-prop)) clojure.lang.Symbol) (list (first output-prop)) (first output-prop))
          (set/union (set [(if (= (count cur-prop) 1) (first cur-prop) cur-prop)]) cur-kb output-prop))))
        )
  )


;; Main test codes
(fwd-infer '(if a b) '#{(not b)})
(fwd-infer '(a) '#{(if a b) (if b c)})
(fwd-infer '(and (not (not (if a b))) a) '#{})

;; Sample test codes
;(fwd-infer '(not (not (not a))) '#{b})
;(fwd-infer '(not (not (and a b))) '#{c})
;(modus-ponens '(a) '#{a b c (if a b)})
;(modus-ponens '(a) '#{a (if a b)})
;(modus-ponens '(a) '#{a b})
;(fwd-infer '(if a b) '#{a})
;(fwd-infer '(a) '#{(if a b)})
;(fwd-infer '(a) '#{(if a b) (if b c)})